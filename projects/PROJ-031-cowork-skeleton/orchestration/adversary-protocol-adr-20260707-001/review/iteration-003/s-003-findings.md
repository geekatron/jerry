# Steelman Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

## Navigation

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable, criticality, protocol |
| [Summary](#summary) | Overall steelman assessment |
| [Step 1: Charitable Interpretation](#step-1-charitable-interpretation) | Core thesis, strongest reading first (H-16) |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation vs. structural vs. evidence vs. substantive |
| [Steelman Reconstruction (Targeted)](#steelman-reconstruction-targeted) | Strengthened language for each surviving gap |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Conditions under which the ADR is most compelling |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Full detail for Major findings |
| [Scoring Impact](#scoring-impact) | Effect of improvements per S-014 dimension |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
- **Deliverable Type:** ADR (Nygard format, L0/L1/L2)
- **Criticality Level:** C3 (auto-escalated per AE-003 new-ADR rule; this ADR itself declares c-007 "auto-C3 minimum")
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (S-003) | **Date:** 2026-07-07 | **Iteration:** 3 (blind — no prior iteration-003 sibling reports read)
- **Note on scope:** This is iteration 3 of a VERIFIED-CRITICALS review of an ADR that is *itself about* the VERIFIED-CRITICALS protocol. The ADR's own changelog (v0.1→v0.3) shows two prior remediation passes already closed 20+ DA/CC/CV findings (false "18 files," self-contradictory tool tier, mis-attributed catch, cost-model inversion, etc.). This steelman therefore charitably assumes that ground has already been covered and looks only for gaps that *survive* that remediation.

---

## Summary

**Steelman Assessment:** The ADR is already a strongly steelmanned artifact in its own right — its Options Considered section runs an explicit steelman-then-rebut pattern on every rejected option (D-1 through D-6), its evidence chain is unusually dense with direct file+line citations that independently verify against the primary score reports (spot-checked below), and its own changelog documents an honest, non-defensive self-correction discipline (disclosing a false "18 files" claim, an inverted cost formula, and a mis-attributed catch, rather than silently fixing them). The core argument — that blind tournaments without an independent verification gate manufacture a non-convergent Critical stream, and that a 3-lens, criticality-gated refutation panel is the minimum-machinery fix — is well-supported and, on the evidence read, correct.
**Improvement Count:** 0 Critical, 4 Major, 2 Minor
**Original Strength:** HIGH. This is a mature, already-twice-remediated C4-evidence-base ADR; remaining gaps are refinements to an already sound argument, not defects that undermine it.
**Recommendation:** Incorporate the 4 Major improvements before this ADR is treated as ready for a critique-strategy pass (S-002/S-004/S-001) per H-16; the 2 Minor items are optional polish.

---

## Step 1: Charitable Interpretation

**Core thesis:** A blind adversarial tournament that counts every claimed Critical finding at face value does not converge — it manufactures a roughly constant stream of Critical-severity claims per round regardless of the document's actual defect count, which the 18-round empirical record demonstrates via a) a declining composite despite zero regressions (fu-log iteration-006, verified independently below) and b) a fabricated "verified" claim surviving four rounds. The fix — an independent, criticality-proportional, 2-of-3-majority refutation panel between claim and score — is empirically shown (iteration-9: 0.68→0.86; iteration-8 FU-log: 0.51→0.72; both independently re-derived from the primary score reports, see spot-checks below) to restore convergence while preserving genuine defects (`DA-002-i8`, confirmed 3-of-3) and discarding manufactured or restated ones (`PM-001-iter8`, refuted 0-of-3).

**Key claims, independently spot-checked against the primary evidence corpus (not merely the ADR's own citations):**

| ADR claim | Corpus location checked | Verified? |
|---|---|---|
| "10 claimed Criticals, 5 VERIFIED / 5 REFUTED... 0.86 vs 0.68" (Context, iter-9) | `adr-convention-20260702-001/adversary/iteration-009/s-014-quality-score.md:36-51` | **Matches exactly.** |
| "15 refutation-panel files = 3 lenses × 5 Critical-bearing reports" (Cost model) | Same file, line 51 ("15 refutation-panel files"); independently confirms 5 distinct reports carry the 10 claimed Criticals (S-001×2, S-002×2, S-004×2, S-011×1, S-012×3) | **Matches.** |
| "12 verification-panel files" (disclosed-correction footnote, Context) | `Glob` on `fu-log-convention-20260705-001/.../iteration-008/verify/*` returns exactly 12 files (3 lenses × 4 reports: s-001, s-002, s-004, s-012) | **Matches — direct filesystem count confirms the ADR's corrected figure, not the source report's self-contradictory "18."** |
| "6 claimed Criticals... DA-001-i8, DA-002-i8, PM-002-iter8, RT-001-20260706-iter8, FM-001/002-i008fmea VERIFIED; PM-001-iter8 REFUTED 0-of-3" (fu-log iter-8) | `fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md:54-55, 65-71` | **Matches exactly**, including the DA-002-i8 3-of-3 unanimous panel result. |
| "iteration-10: 0 VERIFIED, 6 REFUTED... three of four [recurrence] findings' factual lenses VERIFIED; 013-001 refuted even at the factual layer" | `adr-convention-20260702-001/adversary/iteration-010/s-014-quality-score.md:45-56` | **Matches exactly** — 002-001/012-004/CV-001-i010 all VERIFIED at the factual lens; 013-001 REFUTED unanimously including factual. |

No fabricated or misattributed evidence was found in this spot-check. The ADR's own iteration-1/2 self-corrections (false "18," mis-attributed catch, inverted cost formula) are themselves independently confirmed against the primary sources rather than merely trusted.

**Strengthening opportunities (not failures):** the residual gaps below are in the *forward-looking design specification* (D-1 boundary criteria, D-6 tool-tier rationale, the not-yet-built S-016 rubric) rather than in the *evidentiary record*, which is exceptionally solid.

---

## Step 2: Weakness Classification

| Weakness | Type | Magnitude |
|----------|------|-----------|
| D-6's "Write, no Edit" guardrail against overwriting prior verdict files is behavioral (`forbidden_actions`), not tool-tier-structural — in tension with the ADR's own Force 6 / L2 "architecture, not discipline" thesis | Structural / Internal Consistency | Major |
| The proposed Remediation-Value lens rubric conflates "does fixing this matter" with "can this be fixed without new machinery," risking a subtraction-doctrine bias baked into the verification gate itself | Structural (rubric design) | Major |
| WI-8's acceptance criteria validate that the panel *mechanism* works at C3, not that C3 *needs* panels while C1/C2 does not — the AC doesn't actually test the D-1 boundary it is offered to validate | Structural / Methodological Rigor | Major |
| The disclosed C1/C2 residual-spiral risk (Positive Consequence #4) is never connected to RT-M-010's existing iteration ceilings (C1=3, C2=5), which already bound that risk's blast radius — an available mitigation left unstated | Evidence / Completeness | Major |
| "C4 all Criticals" vs. "C3 Criticals only" (D-1 table, Fig. 1, L1 item 4) use two different phrases for what D-2 establishes is the identical scope (all claimed Criticals, no Majors, at both tiers) | Presentation | Minor |
| The Alignment table's "Reversibility: HIGH... remove the adv-verifier invocation and the pipeline reverts to status quo" does not mention that D-2/D-5's adv-scorer edits (dual-protocol, delta-reconciliation) would also need reverting for a true full reversion | Presentation / Traceability | Minor |

All six weaknesses are in specification/presentation, not in the core thesis or the evidentiary record — none require changing the six chosen decisions (D-1 through D-6).

---

## Steelman Reconstruction (Targeted)

Per Section 5's CR-002 adaptation, and because this ADR has already been steelmanned across two remediation iterations, the reconstruction below is targeted to the surviving gaps rather than a full rewrite.

### [SM-001] D-6 tool-tier rationale — reconcile "architecture not discipline" with the Write-guardrail

**Original** (`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:647-656`):
> "Tool tier T2, tools restricted to `Read, Glob, Grep, Write`... must NEVER `Edit` the deliverable or any prior verdict file... P-003 safety (no spawn) and blindness are preserved by the `disallowedTools`/`forbidden_actions` set, not by withholding `Write`."

**Strengthened:**
> "Tool tier T2, tools restricted to `Read, Glob, Grep, Write`... must NEVER `Edit` the deliverable or any prior verdict file... **`Edit`/`Bash`/`Agent` exclusion is enforced structurally via `disallowedTools` (L3 pre-tool gate, deterministic); the narrower 'never overwrite an existing verdict file' property is enforced behaviorally via `forbidden_actions`, because Claude Code's tool model has no 'write-if-not-exists' primitive to express it structurally. This residual behavioral dependency is small in practice — the one-invocation-per-lens-per-report contract (L1 item 1) means each lens's output path is written exactly once per round by construction, so accidental overwrite requires an out-of-contract re-invocation, not routine operation — but it is honestly named here rather than folded into the 'architecture, not discipline' claim made elsewhere (Force 6, L2 Architectural Implications) as if fully structural.**"

**Rationale:** The ADR's own L2 section argues independence must be "structural... rather than behavioral (degrades with fill)" as the central lesson of the fabricated-verification incident. Applying that same standard to its own agent design (rather than only to the verification *stage* as a whole) closes a small but real self-referential gap and pre-empts an S-002/S-007 challenge on this exact point.

**Best Case Conditions:** This strengthening costs nothing to implement (documentation only) and removes the only place in the ADR where a "not merely behavioral" claim is made without the same caveat the rest of the document applies rigorously.

---

### [SM-002] S-016 Remediation-Value lens — separate "matters" from "cheap to fix"

**Original** (`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:691-692`):
> "**Remediation-value lens** — would fixing it change observable behavior, and can it be fixed without adding machinery?"

**Strengthened:**
> "**Remediation-value lens** — would fixing it change observable behavior? **This is the sole VERIFY/REFUTE criterion for the lens.** Whether the fix is subtraction-first (per D-3) or would require new machinery is recorded as a *secondary, non-gating annotation* on the verdict (informing the owner's remediation approach, not the panel's verdict) — this prevents a genuinely important, behavior-changing defect whose only available fix happens to require new machinery from being refuted on remediation-value grounds, which would silently import D-3's remediation *doctrine* into D-1's verification *gate* and undermine Positive Consequence #3 ('genuine regressions preserved') in exactly the scenario where it matters most."

**Rationale:** The empirical record (`DA-002-i8`, a code-logic bug fixed without new machinery) never tests the case where a real, behavior-changing defect's only fix requires new machinery. As specified, the rubric would let the panel refute such a finding under the "can it be fixed without adding machinery" clause even if it clearly changes observable behavior — a false-negative pathway the empirical record does not rule out because it never arose in the n=2, all-text-fix corpus. Separating the gating criterion (behavior change) from the doctrinal annotation (subtraction-first preference) closes this before the not-yet-built S-016 template ships with an untested conflation baked in.

**Best Case Conditions:** Strongest when read against RSK-1 (verifier leniency false-negative) — this finding identifies a *specific, structural* mechanism by which RSK-1 could be realized (not just generic panel leniency) and the fix is a one-clause rubric edit, not a new decision.

---

### [SM-003] WI-8 acceptance criteria — test the boundary, not just the mechanism

**Original** (`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:852`):
> "Run one **C3** tournament using `adv-verifier` to validate the provisional C3 boundary (D-1)... confirm ≥1 claimed Critical is correctly refuted and ≥1 correctly verified... disposition table produced; dual-protocol composites reported."

**Strengthened:**
> "Run one **C3** tournament using `adv-verifier` to validate the provisional C3 boundary (D-1)... confirm ≥1 claimed Critical is correctly refuted and ≥1 correctly verified [mechanism-functions check]. **Additionally, to actually test the D-1 boundary rather than only the panel mechanism: (a) record whether the C3 round exhibits the non-convergent fresh-stream signature (D-4) that motivated gating panels onto C3/C4 in the first place — i.e., would this round, run *without* panels, have shown the same declining-score/manufactured-Critical pattern observed at C4? (b) if feasible within WI-8's scope, run one comparably-sized C2 tournament *without* panels as an informal counterfactual, to begin building the evidence base D-1 itself concedes is currently zero at C1-C2.** ... disposition table produced; dual-protocol composites reported."

**Rationale:** As written, WI-8's AC would be satisfied by any C3 tournament where the panel correctly sorts real from fake Criticals — that is a test of whether `adv-verifier` *works*, not of whether C3 *needs* it more than C1/C2 does. D-1's own honest framing ("the C3 boundary is therefore provisional," line 314-316) commits to validating the boundary, but the AC as drafted cannot falsify the boundary choice — it can only confirm the panel functions, which iteration-9/iteration-10/fu-log-8 already demonstrated at C4. Closing this gap materially strengthens the "reasoned precaution, not yet a finding" framing D-1 already uses honestly elsewhere.

**Best Case Conditions:** The (b) counterfactual is optional/stretch — if WI-8's scope or budget cannot accommodate it, the ADR should say so explicitly rather than let the AC silently under-deliver on the validation it promises.

---

### [SM-004] Positive Consequence #4 — connect the C1/C2 residual risk to its existing bound

**Original** (`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:785-788`):
> "**Cost proportionality.** C1–C2 work pays nothing; the panel budget concentrates on C3/C4 governance, where the spiral was actually *observed* in the record. Per D-1, the C1–C2 exemption is a cost-proportionality decision, **not** an evidence-based finding that C1–C2 tournaments do not exhibit the same (criticality-agnostic, per Forces #1) spiral."

**Strengthened:**
> "**Cost proportionality.** C1–C2 work pays nothing; the panel budget concentrates on C3/C4 governance, where the spiral was actually *observed* in the record. Per D-1, the C1–C2 exemption is a cost-proportionality decision, **not** an evidence-based finding that C1–C2 tournaments do not exhibit the same (criticality-agnostic, per Forces #1) spiral. **This residual exposure is partially bounded independently of this ADR: RT-M-010's existing iteration ceilings (C1=3, C2=5) already cap how many rounds an unverified C1/C2 tournament can spiral through before mandatory escalation, versus C3=7/C4=10's larger window — so the worst case at C1/C2 is a shorter, cheaper unproductive loop, not an unbounded one. This is a partial mitigation, not full closure: a 3-round C1 spiral can still waste a full engagement's review budget on manufactured findings, and no monitoring signal (unlike the Phase-2 trigger for C3/C4, L2 Evolution path) currently exists to detect it. WI-8 or a follow-on work item MAY extend the trigger-gate monitoring to C1/C2 if this residual becomes observable in practice.**"

**Rationale:** The ADR is already careful to disclose the C1/C2 exemption honestly as a cost decision, not a safety finding — this strengthening simply completes that honest picture by naming the one mitigation that already exists in the framework (RT-M-010) rather than leaving the residual risk implicitly unbounded when it is not. This is a Completeness improvement, not a challenge to the decision.

**Best Case Conditions:** Costs nothing (documentation only); directly answers the natural "then why is C1/C2 safe?" question a reader would otherwise have to answer for themselves.

---

## Step 4: Best Case Scenario

**Ideal conditions under which this ADR, with the four Major strengthenings incorporated, is most compelling:** the six decisions are read as a coherent, evidence-anchored package rather than six independent choices — D-1's criticality gate only has teeth because D-6's dedicated verifier guarantees independence, which only matters if D-2's severity gating actually withholds gate-blocking weight from refuted claims, which only converges the tournament if D-4's discriminator knows when to stop, which is only auditable if D-5's delta-reconciliation is mandatory, which only stays cheap if D-3's subtraction doctrine keeps the document from generating fresh attack surface every round. Under these conditions — and given the n=2, all-C4, all-ADR-genre evidence base is honestly disclosed as the current limit (RSK-7), with WI-8 named as the pending falsification test — a rational evaluator should have **HIGH** confidence in the six decisions as specified, and **MEDIUM** confidence (pending WI-8) in the specific C3 boundary and the not-yet-built S-016 rubric's remediation-value lens.

**Key assumptions that must hold:** (1) the `adv-verifier` agent, once built, actually achieves dispatch-ordered blindness (CC-002-iter2's ordering-barrier requirement) rather than merely a prompted instruction; (2) the S-016 template's three lenses are genuinely independent rubrics, not restatements of each other; (3) WI-8 is run before the SSOT pointer (WI-7) lands, as its own precondition already requires.

---

## Improvement Findings Table

| ID | Description | Severity | Original (line ref) | Strengthened | Dimension |
|----|-------------|----------|----------------------|---------------|-----------|
| SM-001-iter3 | D-6 "Write, no Edit" guardrail is behavioral, not tool-tier-structural; not caveated against the ADR's own "architecture not discipline" thesis | Major | L1 item 1, lines 647-656 | Adds explicit structural-vs-behavioral caveat (see reconstruction) | Internal Consistency |
| SM-002-iter3 | Remediation-value lens conflates "does it matter" with "cheap to fix," risking a subtraction-doctrine bias baked into the verification gate | Major | L1 item 2, lines 691-692 | Splits gating criterion (behavior change) from doctrinal annotation (fix style) | Methodological Rigor |
| SM-003-iter3 | WI-8 AC validates the panel mechanism, not the C3-vs-C1/C2 boundary it is offered to validate | Major | Work-Item Decomposition, line 852 | Adds a boundary-testing sub-criterion (recurrence-signature check + optional C2 counterfactual) | Actionability |
| SM-004-iter3 | Disclosed C1/C2 residual spiral risk not connected to RT-M-010's existing iteration-ceiling bound | Major | Consequences (Positive #4), lines 785-788 | Names RT-M-010 as a partial, already-existing mitigation; flags absence of a C1/C2 monitoring signal | Completeness |
| SM-005-iter3 | "C4 all Criticals" vs. "C3 Criticals only" — inconsistent phrasing for an identical scope per D-2 | Minor | D-1 table (line 439), Fig. 1 (lines 511-513), L1 item 4 (lines 700-701) | Align to one phrase, e.g. "all claimed Criticals (no Majors)" at both C3 and C4 | Internal Consistency |
| SM-006-iter3 | Reversibility claim omits that D-2/D-5's adv-scorer edits also need reverting for a true full reversion | Minor | Alignment table, line 471 | Add "(and the D-2/D-5 adv-scorer edits, if a full reversion to status quo is intended)" | Traceability |

**Finding ID Format:** `SM-{NNN}-iter3` (execution-scoped to this iteration-3 blind review pass).

---

## Improvement Details

### SM-001-iter3 (Major, Internal Consistency)

- **Affected Dimension:** Internal Consistency (also touches Methodological Rigor)
- **Original Content:** "P-003 safety (no spawn) and blindness are preserved by the `disallowedTools`/`forbidden_actions` set, not by withholding `Write`." (line 655-656)
- **Strengthened Content:** See [SM-001 reconstruction](#sm-001-d-6-tool-tier-rationale--reconcile-architecture-not-discipline-with-the-write-guardrail) above.
- **Rationale:** The ADR elsewhere (L2 Architectural Implications) makes "structural, not behavioral" the central lesson of the fabricated-verification incident and the reason a dedicated agent (D-6 option A) beats scorer-side verification (D-6 option B, rejected in D-1 too). Applying the same rigor to its own tool-tier design — naming precisely which part is structural (Edit/Bash/Agent exclusion via `disallowedTools`) and which part is behavioral (overwrite prevention via `forbidden_actions`) — is a small, no-cost fix that removes the one place this standard is applied inconsistently to the ADR's own proposal.
- **Best Case Conditions:** Applies whenever a future reader or reviewer takes the "architecture, not discipline" claim at face value and checks it against D-6's own specification — this strengthening survives that check.

### SM-002-iter3 (Major, Methodological Rigor)

- **Affected Dimension:** Methodological Rigor (also touches Evidence Quality — the untested edge case)
- **Original Content:** "would fixing it change observable behavior, and can it be fixed without adding machinery?" (lines 691-692)
- **Strengthened Content:** See [SM-002 reconstruction](#sm-002-s-016-remediation-value-lens--separate-matters-from-cheap-to-fix) above.
- **Rationale:** The empirical record supporting "genuine regressions preserved" (`DA-002-i8`) is a case where the fix happened to be subtraction-compatible; the record contains no case testing what happens when a real, behavior-changing defect's only fix requires new machinery. As specified, the rubric could refute exactly that case, which would be a silent, untested failure mode of the exact property (Positive Consequence #3) the ADR credits to this lens.
- **Best Case Conditions:** Matters most under RSK-1 (verifier leniency false-negative) — this finding narrows a generic risk into a specific, fixable rubric-design flaw.

### SM-003-iter3 (Major, Actionability)

- **Affected Dimension:** Actionability (the AC as written doesn't deliver the validation D-1 promises)
- **Original Content:** WI-8's AC (line 852), quoted above.
- **Strengthened Content:** See [SM-003 reconstruction](#sm-003-wi-8-acceptance-criteria--test-the-boundary-not-just-the-mechanism) above.
- **Rationale:** D-1's rationale (lines 314-316) explicitly frames WI-8 as validating *the boundary* ("C3 panels, C1-C2 none"), not merely confirming the panel mechanism works when pointed at a C3 document. Mechanism-correctness was already demonstrated at C4 (iteration-9/10, fu-log-8); WI-8 as scoped would re-demonstrate the same thing one tier down without answering the actual open question (does C3 need panels more than C1/C2 does?).
- **Best Case Conditions:** The optional (b) counterfactual is the ideal case; even without it, adding the recurrence-signature check (a) meaningfully closes the gap between what WI-8 claims to validate and what its AC actually tests.

### SM-004-iter3 (Major, Completeness)

- **Affected Dimension:** Completeness
- **Original Content:** Positive Consequence #4 (lines 785-788), quoted above.
- **Strengthened Content:** See [SM-004 reconstruction](#sm-004-positive-consequence-4--connect-the-c1c2-residual-risk-to-its-existing-bound) above.
- **Rationale:** The ADR is unusually disciplined about disclosing this exact risk as a cost decision rather than a safety finding — the strengthening simply completes the honest picture already in progress by naming RT-M-010 as a partial, pre-existing mitigation and flagging the absence of any monitoring signal for C1/C2 (unlike the explicit Phase-2 trigger-gate for C3/C4). This is additive disclosure, not a reversal of the decision.
- **Best Case Conditions:** Strongest as a pre-emptive answer to the natural "why is C1/C2 safe, then?" question a Devil's Advocate pass would otherwise raise.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-004 closes an unstated-mitigation gap in the risk disclosure. |
| Internal Consistency | 0.20 | Positive | SM-001 and SM-005 remove two self-referential inconsistencies (architecture-vs-discipline claim; C4/C3 phrasing). |
| Methodological Rigor | 0.20 | Positive | SM-002 removes an untested conflation from a not-yet-built rubric before it ships; SM-003 makes WI-8 actually test what D-1 says it will test. |
| Evidence Quality | 0.15 | Neutral | Already exceptionally strong — spot-checks in Step 1 found zero fabricated or misattributed citations; no improvement needed here beyond SM-002's edge-case note. |
| Actionability | 0.15 | Positive | SM-003 makes the WI-8 acceptance criteria deliver the validation the ADR promises, not merely a mechanism smoke-test. |
| Traceability | 0.10 | Positive (minor) | SM-006 completes the reversibility claim's scope. |

**Impact key:** Positive = directly strengthened by an incorporated improvement; Neutral = already adequate; Negative = none identified.

---

*Steelman execution complete. 0 Critical / 4 Major / 2 Minor findings. All six chosen decisions (D-1 through D-6) remain sound as specified; findings target specification-level gaps in the not-yet-built S-016 rubric, the D-6 tool-tier rationale, one work-item's acceptance criteria, and two presentation/traceability polish items. Recommended: incorporate before S-002/S-004/S-001 critique passes per H-16 (already satisfied — S-003 precedes; downstream strategies should treat these 4 Majors as the current strongest-form baseline).*
