# Quality Score Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology) — Iteration 2

## Navigation

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Plain-language verdict and top action item |
| [Scoring Context](#scoring-context) | Deliverable, criticality, protocol, inputs read |
| [VERIFIED-CRITICALS Panel Reconciliation](#verified-criticals-panel-reconciliation) | Panel outcome, per-lens tallies, dedup mapping |
| [Score Summary](#score-summary) | Dual-protocol composite, threshold, verdict |
| [Dimension Scores](#dimension-scores) | Weighted 6-dimension table |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement path per dimension |
| [Delta-Reconciliation](#delta-reconciliation) | Explicit comparison against iteration-1 (0.66) |
| [Disclosed Residuals (Advisory)](#disclosed-residuals-advisory) | Unrefuted/out-of-scope Majors/Minors — advisory, not gating |
| [Improvement Recommendations](#improvement-recommendations-priority-ordered) | Priority-ordered, mapped to VERIFIED Criticals |
| [Leniency Bias Check](#leniency-bias-check) | H-15 self-review |
| [Session Context Handoff](#session-context-handoff) | Structured summary for orchestrator |

---

## L0 Executive Summary

**Composite (VERIFIED protocol):** 0.65/1.00 | **Composite (old protocol):** 0.63/1.00 | **Verdict:** REVISE
**Verified Criticals:** 6 of 7 claimed Criticals (86%) | **Weakest Dimension:** Internal Consistency (0.55)

**One-line assessment:** The iteration-1 remediation genuinely closed 2 of its 4 underlying defects (the RSK-1 mitigation inversion and the "18 vs 12" file-count citation both hold up clean under independent re-check this round) but only partially closed a third (the criticality-evidence-overreach hedge was added to D-1's own text but never propagated to the Positive Consequences bullet it left just as overclaiming) and did not actually close the fourth (the cost-model/invocation-contract granularity contradiction was re-worded into internal consistency but the new wording is falsified by the very empirical file counts cited to support it) — while three brand-new Critical-severity defects surfaced in material the remediation itself touched or left untouched, including the ADR's own flagship evidentiary anecdote for its central proposal, D-1/D-6, being independently shown to misattribute the mechanism that caught the fabricated PR-template claim. The net effect is the composite holding essentially flat against iteration 1 (0.66 → 0.65): genuine partial progress, offset by fresh residuals of the very fix that produced it — precisely the "closes the specific instance... but has not yet closed the class of problem" pattern this ADR's own Context section quotes from the empirical record it is trying to formalize a defense against.

**Dual-protocol note:** 6 of the 7 claimed Criticals this round (86%) were VERIFIED — a markedly higher hold-up rate than the ADR's own cited historical rounds (iter-9: 50%; iter-8 FU: 86%; iter-10: 0%), meaning this iteration's finder strategies were not manufacturing claims. The one claimed Critical excluded from verified-protocol weight (S-003 Steelman's SM-001) was not routed through a panel — it restates, from a different angle, the same underlying cost-model/evidence gap already carried by the VERIFIED DA-001-i2, so its exclusion changes little; the small 0.02-point protocol delta (0.65 vs 0.63) reflects that narrow redundancy, not a large discard of manufactured claims.

---

## Scoring Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` (v0.2, iteration-1 remediation applied)
- **Deliverable Type:** ADR (Nygard format, L0/L1/L2), status PROPOSED
- **Criticality Level:** C3 (per invoking task; ADR self-declares auto-C3-minimum at its own c-007)
- **Scoring Strategy:** S-014 (LLM-as-Judge), VERIFIED-CRITICALS protocol, iteration 2
- **SSOT Reference:** `.context/rules/quality-enforcement.md` (Quality Gate, 6-dimension weighted composite)
- **Quality Threshold:** >= 0.92 (H-13)
- **Inputs read:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` (deliverable, full text, 866 lines)
  - `.../review/iteration-002/s-003-findings.md` (S-003 Steelman: 1 Critical, 1 Major, 1 Minor)
  - `.../review/iteration-002/s-002-findings.md` (S-002 Devil's Advocate: 3 Critical, 2 Major, 1 Minor)
  - `.../review/iteration-002/s-007-findings.md` (S-007 Constitutional AI Critique: 1 Critical, 2 Major, 1 Minor)
  - `.../review/iteration-002/s-011-findings.md` (S-011 Chain-of-Verification: 2 Critical, 1 Major)
  - `.../review/iteration-002/verify/{s-002,"s-007 (constitutional ai critique)",s-011}-{factual,materiality,remediation-value}.md` (9 refutation-panel files, one triplet per Critical-bearing report)
  - `.../review/iteration-001/s-014-quality-score.md` (prior score, 0.66, for delta-reconciliation)
- **Prior score:** 0.66 (iteration 1) — see [Delta-Reconciliation](#delta-reconciliation)

---

## VERIFIED-CRITICALS Panel Reconciliation

Per the ADR's own D-1/D-2 decision (applied to its own review, consistent with the dogfooding named in its Meta-Note), every claimed Critical was adjudicated by a 3-lens blind refutation panel (factual-accuracy / materiality / remediation-value), 2-of-3 majority, DEFAULT-REFUTED. The S-003 Steelman finding (SM-001, Critical) was **not** routed through a panel this round — no `verify/` files exist for the S-003 report — and per the commissioning instruction's explicit panel outcome, it carries **no weight** this iteration (treated as the protocol's DEFAULT-REFUTED-on-uncertainty posture).

### Per-lens tally

| Finding ID | Source Strategy | Factual | Materiality | Remediation-Value | Majority | **Panel Verdict** |
|---|---|---|---|---|---|---|
| DA-001-i2 | S-002 | VERIFIED | VERIFIED | VERIFIED | 3-of-3 | **VERIFIED** |
| DA-002-i2 | S-002 | VERIFIED | VERIFIED | VERIFIED | 3-of-3 | **VERIFIED** |
| DA-003-i2 | S-002 | VERIFIED | VERIFIED | VERIFIED | 3-of-3 | **VERIFIED** |
| CC-001-iter2 | S-007 | VERIFIED | VERIFIED | VERIFIED | 3-of-3 | **VERIFIED** |
| CV-001-20260707 | S-011 | VERIFIED | VERIFIED | VERIFIED | 3-of-3 | **VERIFIED** |
| CV-002-20260707 | S-011 | VERIFIED | VERIFIED | VERIFIED | 3-of-3 | **VERIFIED** |
| SM-001-20260707T-iter002 | S-003 | — (no panel run) | — | — | n/a | **NOT VERIFIED (no weight)** |

**Result: 6 of 7 claimed Criticals VERIFIED, unanimous 3-of-3 on every panelled item. 0 REFUTED. 1 unpanelled (SM-001).** Majors/Minors (DA-004-i2, DA-005-i2, DA-006-i2, CC-002-iter2, CC-003-iter2, CC-004-iter2, CV-003-20260707, SM-002, SM-003) remain outside the Critical-only panel gate. Of these, CC-002-iter2/CC-003-iter2/CC-004-iter2 were explicitly reviewed and **REFUTED** by the S-007 materiality lens (which extended beyond its mandatory scope to cover all four S-007 findings); the remainder are unrefuted/out-of-scope advisory inputs — see [Disclosed Residuals](#disclosed-residuals-advisory).

### Dedup / continuity mapping against iteration-1's 4 underlying defects

| Iteration-1 underlying defect | Iteration-1 disposition (per changelog v0.2) | Iteration-2 finding | Status this round |
|---|---|---|---|
| RSK-1 mitigation inversion (DA-004-i1/CC-001-i1) | Rewritten: discard-biased framing, named partial counterweights | *(none — not re-raised)* | **Genuinely closed, 0 recurrence** |
| False "18 vs 12" verifier-file citation (DA-001-i1/CV-001-i1) | Corrected at 3 sites + disclosed-correction footnote | *(none — not re-raised; both S-003 and S-007 iter-2 independently re-confirmed "12" is now accurate)* | **Genuinely closed, 0 recurrence** |
| Criticality-gating evidence overreach (DA-003-i1) | D-1 text hedged as "reasoned default, not a finding"; WI-8 provisional-validation language added | **DA-002-i2** (VERIFIED) — the hedge was added to D-1 but not propagated to Positive Consequence #4, which still states the spiral "actually occurs" at C3/C4 as settled fact | **Partially closed — recurrence in a different location, same root claim** |
| Cost-model/invocation-contract granularity contradiction (DA-002-i1/CC-002-i1/CV-002-i1, 9-of-9 sub-verdict convergence) | "Standardized" wording to "3 x claimed Criticals" across all 6 sites | **DA-001-i2** (VERIFIED) — the wording is now internally consistent, but it is falsified by the very empirical file counts (12, 15) cited to support it, which actually reconcile as per-*report*, not per-claimed-Critical | **Not closed — the fix moved the contradiction from text-vs-text to text-vs-evidence** |
| *(new this round)* | — | **CC-001-iter2** — `adv-verifier`'s T1 (read-only) tool tier structurally excludes `Write`, yet its output contract mandates persisting per-lens verdict files | **Fresh, previously-uncaught defect** |
| *(new this round)* | — | **CV-001-20260707** — the flagship fabricated-PR-template anecdote (the ADR's own "strongest argument for independent verification") is attributed to the new refutation panel, but the primary source shows it was caught by an ordinary S-001 Red Team finder pass, not any panel | **Fresh, previously-uncaught defect** |
| *(new this round)* | — | **CV-002-20260707** — Figure 3's stop-condition routing lets a VERIFIED Critical bypass the `FIX` node on a fresh-stream/already-verified-protocol branch, contradicting D-2's unconditional gating and Figure 2's own unconditional pathway | **Fresh, previously-uncaught defect** |
| **DA-003-i2** (new gap in newly-added material) — RSK-7 was itself *added* during the iteration-1 remediation (as the advisory fix for DA-005-i1), but its prose mitigation ("WI-8 required before framework-general adoption") is not encoded as a WI-7 dependency | **Fresh gap inside the iteration-1 fix's own new material** |

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite (VERIFIED protocol)** | **0.65** |
| **Weighted Composite (old protocol — all 7 claimed Criticals gate, no verification discount)** | **0.63** |
| **Threshold** | 0.92 (H-13) |
| **Verdict** | **REVISE** (score-band REVISE at 0.50–0.69, *and* automatic-REVISE per 6 VERIFIED Criticals — both triggers agree) |
| **Strategy Findings Incorporated** | Yes — 4 finder reports (S-003, S-002, S-007, S-011) + 9 refutation-panel files |
| **Verified Criticals** | 6 of 7 claimed (86%) |

**Why the two protocols are close but not identical this round:** unlike iteration 1 (where 0/8 claimed Criticals were discarded, so both protocols converged exactly), this round has one unpanelled claimed Critical (SM-001) that would count at full weight under the old, unconditional "any Critical -> REVISE" rule (`skills/adversary/agents/adv-scorer.md:166-167`). Because SM-001 substantively restates DA-001-i2's already-VERIFIED cost-model finding rather than raising an independent defect, its exclusion produces only a small (~0.02) delta rather than the 0.18-0.21-point gaps the ADR's own cited historical rounds show for genuinely discarded (manufactured/restated) claims — itself a data point consistent with this round's high (86%) verification rate.

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-------------------|
| Completeness | 0.20 | 0.82 | 0.164 | Structure unchanged and still comprehensive (Nygard L0/L1/L2, 4 diagrams, 6 steelmanned decisions, 8-item WI decomposition); the iteration-1 fix added RSK-7 + WI-8 non-ADR-genre language, a genuine completeness improvement, though its own wiring gap is scored under Traceability/Actionability, not here. |
| Internal Consistency | 0.20 | 0.55 | 0.110 | Weakest dimension, unchanged from iteration 1. 3 of 6 VERIFIED Criticals land here: DA-001-i2 (cost-model wording vs. its own cited evidence), DA-002-i2 (Positive Consequence #4 vs. D-1's own hedge), CV-002-20260707 (Figure 3 vs. D-2/Figure 2). Two of the three are direct residues of iteration-1's own remediation. |
| Methodological Rigor | 0.20 | 0.60 | 0.120 | CC-001-iter2 (VERIFIED, unanimous): the D-6 agent-design decision — the ADR's central proposed new agent — is not executable as specified (T1 tool tier structurally excludes the `Write` its own output contract requires). CV-002-20260707 lands here secondarily (a "mmdc-validated" figure's stop-condition logic is unsound as drawn). Overall Nygard methodology (steelman-first, six-decision structure) remains otherwise sound. |
| Evidence Quality | 0.15 | 0.55 | 0.0825 | CV-001-20260707 (VERIFIED, unanimous): the ADR's single most emphasized evidentiary anecdote ("The strongest argument for independent verification is a concrete failure") misattributes the catching mechanism to the new panel when the primary source shows an ordinary pre-existing finder strategy (S-001 Red Team) made the catch. DA-001-i2 (cost-model empirical basis) also lands here. Offsetting positive: every other spot-checked citation (composites, panel splits, the corrected "12" file count, DA-002-i8 regression, RSK-1 rewrite) independently re-verified accurate this round (per both S-007 and S-011 methodology notes). |
| Actionability | 0.15 | 0.63 | 0.0945 | CC-001-iter2: WI-1's acceptance criteria require both "T1 tools only" and "per-lens verdict files persisted" simultaneously — an implementer cannot satisfy both as written. DA-003-i2 also touches actionability (RSK-7's mitigation is not wired into an executable work-item gate). Unrefuted advisory Majors (DA-004-i2, DA-005-i2) additionally flag unscheduled risk-closure and an unbounded Critical-heavy-round cost path. |
| Traceability | 0.10 | 0.62 | 0.062 | DA-003-i2 (VERIFIED, unanimous, primary dimension): RSK-7's prose mitigation ("WI-8 required... before the protocol is treated as framework-general") is not encoded in the Work-Item Decomposition table's own "Depends on" column — WI-7 lists only WI-2/WI-3; a reader cannot derive the enforced gate from the table other rows do use for exactly this purpose (e.g., WI-3 -> WI-1). Citation discipline otherwise remains strong (independently re-verified by 3 separate blind strategies this round). |
| **TOTAL** | **1.00** | | **0.6475 -> 0.65** | |

---

## Detailed Dimension Analysis

### Completeness (0.82/1.00)

**Evidence:** All Nygard sections remain present and populated; the iteration-1 remediation pass added net-new completeness (RSK-7 external-validity risk register entry, WI-8 non-ADR-genre validation requirement) that did not exist at iteration 1. No VERIFIED Critical this round has Completeness as its primary dimension.

**Gaps:** The completeness gain from adding RSK-7/WI-8 is undercut by DA-003-i2 (scored under Traceability/Actionability): the new material's own promised safeguard is not wired into the executable dependency graph. Unrefuted advisory: DA-005-i2 (structural closure for RSK-1/RSK-2 is an unscheduled Phase-2 idea with no corresponding work item).

**Improvement Path:** Add the WI-7 -> WI-8 dependency edge (closes DA-003-i2's gap, also raising Traceability/Actionability); schedule or explicitly disclaim Phase 2 as a work item (DA-004-i2 advisory).

---

### Internal Consistency (0.55/1.00)

**Evidence:** Three independently-corroborated, self-contained textual contradictions, all unanimous 3-of-3 VERIFIED:
1. **DA-001-i2** — c-004/D-6/L1/Cost-model/Fig.4/WI-1 all assert "3 invocations per lens *per claimed Critical*" (cost = 3 x number of claimed Criticals), citing "iter-9 = 15 files = 3x5" and "iter-8 FU = 12 files = 3x4." But the ADR's own Context section states iteration-9 had **10** claimed Criticals (not 5) and iteration-8 FU had **>=7** (not 4) — the "5" and "4" are report counts, not claimed-Critical counts, and the disclosed-correction footnote at line 166 explicitly labels the parallel "4" as "Critical-bearing **reports**" while lines 217/385-386 label the identical figure "Criticals." The stated formula would require 30 and >=21 files respectively, not 15/12.
2. **DA-002-i2** — Positive Consequence #4 ("the spiral actually occurs" at C3/C4) directly contradicts D-1's own careful hedge two sections earlier ("the C1-C2 exemption is a cost-proportionality default... not a finding that C1-C2 'did not spiral'"), compounded by the Forces section's own criticality-agnostic mechanism description.
3. **CV-002-20260707** — Figure 3's stop-condition flowchart routes a VERIFIED Critical around the `FIX` (remediation) node whenever it does not recur across rounds and the verified protocol is already running, contradicting Figure 2's unconditional `Verified -> AutoReviseGate -> Remediated` pathway and D-2's unconditional gating text.

**Gaps:** All three are internal, self-referential contradictions discoverable from the ADR's own text (two of the three are residues of the very remediation intended to fix related iteration-1 defects). None was caught by the ADR's own extensive self-review claims before this round.

**Improvement Path:** (a) Reconcile the cost-model unit to "per Critical-bearing report" at all six sites, matching the actual empirical file counts (per the S-003 Steelman's SM-001 reconstruction, which independently proposes the identical fix). (b) Propagate D-1's "reasoned default, not a finding" hedge into Positive Consequence #4. (c) Remove or gate the Q2/Q3 recurrence branch in Figure 3 so no VERIFIED Critical can reach the ceiling check without first passing through `FIX`.

---

### Methodological Rigor (0.60/1.00)

**Evidence:** CC-001-iter2 (VERIFIED, unanimous across all 3 lenses): the D-6 decision's central artifact — the new `adv-verifier` agent — is specified with a self-contradictory tool tier. T1 (`Read, Glob, Grep`) structurally excludes `Write` per the framework's own SSOT (`.context/rules/agent-development-standards.md`, Tool Security Tiers), yet the same agent's mandatory output contract requires persisting a new file per lens per finding. As written, WI-1 is not buildable without a builder silently resolving the contradiction off-record. CV-002-20260707 lands here secondarily: one of the four "mmdc-validated" figures central to the Decision section contains an unsound stop-condition specification.

**Gaps:** The overall Nygard methodology (six-decision options analysis, steelman-first per H-16, four validated diagrams) remains genuinely rigorous in form; the defect is narrow but load-bearing — it sits in the one place this ADR proposes new agent machinery, which is also the property (independent T1 blindness) the ADR's own Force 6/D-1 rationale calls "load-bearing."

**Improvement Path:** Correct the tool-tier declaration (e.g., "T1 + Write only, no Edit/Bash/Agent" or upgrade to T2 with an added "never edit the deliverable or prior verdict files" forbidden-action) at all three restatement sites (L1 item 1, WI-1, Draft Issue A). Fix Figure 3 per the Internal Consistency remediation above.

---

### Evidence Quality (0.55/1.00)

**Evidence:** CV-001-20260707 (VERIFIED, unanimous): the ADR's Context section states the fabricated PR-template claim "was caught only by the iteration-10 refutation panel's factual lens," repeating the attribution in L1 Item 2 and the Decision Rationale. Independent re-check of the cited primary source (`.../adr-convention-20260702-001/adversary/iteration-010/s-014-quality-score.md`) shows the panel's six adjudicated Criticals do not include the PR-template claim, which is tracked separately as `RT-001-iter010`, sourced from an ordinary **S-001 Red Team** finder pass and explicitly logged as an unrefuted, non-panelled **Major**. This is the ADR's own self-described "strongest argument for independent verification" resting on a misattributed anecdote. DA-001-i2 (cost-model empirical basis) also lands here.

**Gaps:** Both defects are narrow (one anecdote, one cost-model paragraph) rather than pervasive — the S-007 iteration-2 methodology note independently re-verified 8 separate citations this round (composites, file counts, quoted rationale) and found all of them accurate, consistent with the S-003 Steelman's parallel finding that "every other spot-checked quantitative citation... checks out exactly."

**Improvement Path:** Re-attribute the PR-template catch to the actual S-001 Red Team finder pass, and either drop the anecdote as flagship support for D-1/D-6 or reframe it as evidence for the value of continued blind multi-strategy rotation generally (not the new panel specifically). Resolve the cost-model unit per the Internal Consistency fix.

---

### Actionability (0.63/1.00)

**Evidence:** CC-001-iter2: WI-1's acceptance criteria ("T1 tools only" + "per-lens verdict files persisted") cannot both be satisfied by an implementer as literally written — a HARD-adjacent defect (H-34 tool-tier schema validity) in the ADR's central new work item. DA-003-i2 also affects actionability: RSK-7's stated safeguard is not wired into WI-7's dependency criteria, so a team executing the backlog literally could complete WI-7 (the SSOT pointer that operationalizes framework-general adoption) before WI-8's non-ADR-genre validation ever runs.

**Gaps:** Unrefuted advisory Majors compound this: DA-004-i2 (RSK-1/RSK-2's cited "structural closure" is an unscheduled, un-triggered future phase with no work item) and DA-005-i2 (RSK-4's mitigations do not actually bound a single Critical-heavy round/report). Impact remains contained — the ADR states nothing is implemented by this document, so these are pre-implementation specification defects rather than live blockers.

**Improvement Path:** Resolve the tool-tier contradiction (see Methodological Rigor) before WI-1 is opened as a work item; add WI-8 as an explicit WI-7 precondition (or acceptance-criteria clause); schedule Phase 2 as a triggered future work item or explicitly disclaim it; add a per-round/per-report invocation ceiling to RSK-4's mitigation.

---

### Traceability (0.62/1.00)

**Evidence:** DA-003-i2 (VERIFIED, unanimous, primary dimension): RSK-7's mitigation text names WI-8 as a required precondition for "framework-general" treatment, but the Work-Item Decomposition table's own "Depends on" column — the mechanism other rows demonstrably use for exactly this purpose (WI-3 -> WI-1, WI-4 -> WI-2) — does not encode it; WI-7 lists only WI-2/WI-3, and WI-8 does not reference WI-7 either. A reader cannot derive "is the non-ADR-genre validation actually gating adoption?" from the executable plan alone.

**Gaps:** Otherwise strong — citation discipline was independently re-verified by three separate blind strategies this round with zero discrepancies found outside the items above. Unrefuted advisory: SM-003 (Minor — the disclosed-correction footnote does not flag that its own cited source's footer still carries a separate, differently-wrong arithmetic).

**Improvement Path:** Add the WI-7 -> WI-8 dependency edge or an equivalent acceptance-criteria clause so RSK-7's stated mitigation is enforced by the plan a team would actually execute, not just asserted in prose.

---

## Delta-Reconciliation

Per D-5 (mandatory delta-reconciliation against the prior iteration — a standard this ADR itself proposes and which this scoring exercise applies reflexively to its own review), iteration 1 scored **0.66** with 8 of 8 claimed Criticals VERIFIED. This iteration scores **0.65** with 6 of 7 claimed Criticals VERIFIED. The near-zero net delta (-0.01) is **not** evidence of stagnation masking either full remediation or a purely manufactured fresh stream — it is the arithmetic result of two independent, opposite-signed movements:

- **Genuine convergence (positive):** 2 of iteration-1's 4 underlying defects (RSK-1 mitigation inversion; the "18 vs 12" citation) show **zero recurrence** this round under independent re-verification by different blind strategies than found them originally — a clean instance of the "recurrence vs. fresh stream" discriminator (D-4) correctly identifying genuine, durable fixes.
- **Incomplete convergence (negative, partially offsetting):** 1 of iteration-1's 4 defects (criticality-evidence overreach) was only partially propagated (DA-002-i2 recurs in a new location); 1 (cost-model granularity) was re-worded but not actually resolved against its own cited evidence (DA-001-i2 recurs in substance, not merely in wording).
- **Fresh stream (negative):** 3 entirely new Critical-severity defects surfaced this round (CC-001-iter2, CV-001-20260707, CV-002-20260707), none flagged by any of the 4 iteration-1 finder reports, at least one of which (DA-003-i2, RSK-7 wiring) exists inside material the iteration-1 remediation itself introduced.

Per the ADR's own D-4 convergence discriminator, none of this round's findings are recommended for a "switch protocols or stop" response — every claimed Critical this round was independently corroborated as real (86% verification rate, unanimous 3-of-3 on every panelled item), which is the discriminator's "recurring/genuine defect -> remediate" branch, not the "non-convergent manufactured stream" branch. The correct interpretation is that the document is not yet converged, not that the tournament process is malfunctioning.

---

## Disclosed Residuals (Advisory)

The following are unrefuted or out-of-scope Major/Minor findings, outside the Critical-only panel gate (D-1), and therefore **advisory inputs to scoring, not gating findings** — consistent with D-2's "disclosed residuals are valid MEDIUM posture, not findings":

| ID | Source | Severity | Summary | Advisory dimension |
|---|---|---|---|---|
| DA-004-i2 | S-002 | Major | RSK-1/RSK-2's cited "structural closure" (deterministic pre-panel factual lens) is an unscheduled, un-triggered future phase with zero corresponding work item | Actionability |
| DA-005-i2 | S-002 | Major | RSK-4's stated mitigations do not actually bound a single Critical-heavy round/report | Actionability |
| DA-006-i2 | S-002 | Minor | D-1's numeric score gap (C=9 vs B=6) implies a confidence differential the surrounding prose explicitly disclaims | Methodological Rigor |
| CV-003-20260707 | S-011 | Major (out of panel scope) | "Every refutation panel confirmed the factual core is real" overstates iteration-10's grandfather-seam convergence; one of the four cited findings' own factual lens actually REFUTED the underlying premise, not merely its materiality | Evidence Quality |
| SM-002 | S-003 | Major | WI-8's acceptance criteria do not require confirming the built `adv-verifier`'s actual invocation count matches whichever cost formula the ADR ultimately states | Actionability / Traceability |
| SM-003 | S-003 | Minor | The disclosed-correction footnote (18->12) does not flag that its own cited source's footer still carries a separate, differently-wrong arithmetic | Traceability |

**Refuted this round (explicitly reviewed, zero weight):** CC-002-iter2, CC-003-iter2, CC-004-iter2 (all Major/Minor from S-007; the materiality lens extended beyond its mandatory Critical-only scope to review all four S-007 findings and refuted these three as, respectively, a speculative implementation-ordering concern, a defensible SSOT-scoping choice already covered by existing precedent, and a soft draft-convention interpretation ambiguity).

---

## Improvement Recommendations (Priority Ordered)

| Priority | Underlying Defect (VERIFIED Criticals) | Current Impact | Target | Recommendation |
|----------|------|---------|--------|----------------|
| 1 | Methodological Rigor / Actionability (0.60/0.63) — `adv-verifier` T1-vs-persistence contradiction (CC-001-iter2) | D-6's central new agent is not buildable as specified without a silent, unrecorded tier deviation | 0.85+ | Correct the tool-tier declaration at all 3 restatement sites (L1 item 1, WI-1, Draft Issue A) to a tier that includes `Write` (or T2 + an added forbidden-edit guardrail). |
| 2 | Internal Consistency / Methodological Rigor (0.55/0.60) — Figure 3 bypasses remediation (CV-002-20260707) | A "mmdc-validated" central figure contradicts D-2's own unconditional gating rule and Figure 2 | 0.85+ | Remove or gate the post-Q1 recurrence branch in Figure 3 so no VERIFIED Critical can reach the ceiling check without first passing through `FIX`. |
| 3 | Evidence Quality (0.55) — flagship anecdote misattribution (CV-001-20260707) | The ADR's own "strongest argument for independent verification" is shown to be an ordinary finder-strategy catch, not a panel catch | 0.85+ | Re-attribute the PR-template catch to S-001 Red Team, iteration 10; reframe or drop it as flagship support for D-1/D-6. |
| 4 | Internal Consistency / Evidence Quality (0.55) — cost-model unit still unreconciled against its own cited evidence (DA-001-i2) | The going-forward per-Critical invocation contract is untested at the granularity it will actually operate at; ~2x cost-model risk | 0.85+ | Reconcile the unit to "per Critical-bearing report" at all 6 sites (c-004, D-6 rationale, L1 item 1, Cost model, Fig. 4 label, WI-1 AC), matching the actual empirical file counts. |
| 5 | Internal Consistency (0.55) — Positive Consequence #4 vs. D-1's own hedge (DA-002-i2) | A reader who reads only Consequences draws an unsupported empirical conclusion about C3/C4-only spiral occurrence | 0.85+ | Propagate D-1's "reasoned default, not a finding" hedge into the Positive Consequence #4 bullet. |
| 6 | Traceability / Actionability (0.62/0.63) — RSK-7 mitigation not wired into the WI dependency graph (DA-003-i2) | RSK-7's stated safeguard (non-ADR-genre validation before framework-general adoption) is unenforced by the executable plan | 0.85+ | Add WI-8 as an explicit WI-7 dependency or equivalent acceptance-criteria clause. |
| 7 (advisory) | Actionability (0.63) — unscheduled Phase-2 closure, unbounded cost-blowup mitigation (DA-004-i2, DA-005-i2, SM-002) | Two HIGH-impact risk mitigations rest on an un-triggered future phase; WI-8 does not gate on invocation-granularity correctness | 0.85+ | Schedule Phase 2 with a trigger condition or disclaim it; add a per-round invocation ceiling to RSK-4; add an invocation-count reconciliation clause to WI-8. |
| 8 (advisory) | Evidence Quality / Traceability (0.55/0.62) — grandfather-seam overstatement, footnote hygiene (CV-003-20260707, SM-003) | Minor framing/citation-hygiene drift | 0.90+ | Reword the "every... confirmed" sentence to name the one dissenting factual lens; note the source footer's residual arithmetic discrepancy. |

---

## Leniency Bias Check

- [x] Each dimension scored independently against the VERIFIED-Critical evidence before computing the composite
- [x] Evidence documented for each score, with file+line citations reproduced from the underlying finder/panel reports (not re-derived from this scoring pass alone)
- [x] Uncertain scores resolved downward — Internal Consistency and Evidence Quality held at the low end of their "0.5-0.69" bands given the load-bearing nature of the defects (a central figure, a central agent design, and the flagship evidentiary anecdote)
- [x] Second-iteration calibration considered — a near-zero delta against a 0.66 baseline is treated honestly as "not yet converged," not rounded up toward the changelog's own stated "target >=0.92" aspiration
- [x] No dimension scored above 0.95; highest score (Completeness, 0.82) reflects genuine structural strength with real, disclosed gaps remaining
- [x] Automatic-REVISE rule applied independent of composite score: 6 of 6 panelled VERIFIED Criticals unanimous (3-of-3) -> REVISE regardless of where composite fell
- [x] Old-protocol composite computed and reported per the dual-protocol transparency clause (D-2) this ADR itself proposes

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.65
composite_old_protocol: 0.63
threshold: 0.92
weakest_dimension: internal_consistency
weakest_score: 0.55
critical_findings_count: 7
verified_criticals: 6
refuted_criticals: 0
unpanelled_criticals: 1
iteration: 2
prior_score: 0.66
delta: -0.01
improvement_recommendations:
  - "Fix adv-verifier tool-tier self-contradiction (T1 vs. mandatory file persistence) at all 3 sites (CC-001-iter2)"
  - "Remove/gate Figure 3's post-Q1 recurrence branch so no VERIFIED Critical bypasses FIX (CV-002-20260707)"
  - "Re-attribute the fabricated-PR-template catch to S-001 Red Team, iteration 10, not the new panel (CV-001-20260707)"
  - "Reconcile cost-model unit to per-Critical-bearing-report at all 6 sites, matching actual file counts (DA-001-i2)"
  - "Propagate D-1's evidence hedge into Positive Consequence #4 (DA-002-i2)"
  - "Add WI-8 as an explicit WI-7 dependency so RSK-7's mitigation is enforced (DA-003-i2)"
  - "(advisory) Schedule Phase 2 or disclaim it; bound RSK-4's Critical-heavy-round cost; reconcile WI-8's invocation-count check (DA-004-i2/DA-005-i2/SM-002)"
  - "(advisory) Correct grandfather-seam unanimity overstatement and footnote hygiene (CV-003-20260707/SM-003)"
```

---

*Scoring performed per S-014 (LLM-as-Judge), VERIFIED-CRITICALS protocol dogfooded against its own proposing ADR, iteration 2. P-003: no subagents invoked. P-020: all writes confined to `projects/PROJ-031-cowork-skeleton/`; the deliverable itself was not edited by this scoring pass. P-022: every dimension score is tied to file+line evidence reproduced from the four blind finder reports and nine refutation-panel files; inference (e.g., dimension-impact weighting, composite-delta interpretation) is labeled as such and distinguished from independently-verified panel fact. No employer-internal tokens or absolute filesystem paths appear in this report.*
