# Devil's Advocate Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Methodology)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md
**Criticality:** C3 (per invoking task; the ADR itself self-classifies auto-C3-minimum at c-007)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-002 blind execution)
**H-16 Compliance:** This execution ran inside the tournament's declared 6-group blind order
(self-refine -> steelman -> challenge -> verify -> decompose -> score), in which S-003 Steelman
(Group B) precedes the Group C challenge strategies (S-002 is a Group C member). Per this
execution's own task instructions, this agent was run BLIND to all sibling review outputs under
`review/iteration-001/` (including any S-003 output), so it cannot cite the S-003 artifact
directly. **H-16 compliance is therefore assumed at the orchestration level, not independently
verified by this execution** -- flagged as a self-review caveat (H-15) rather than a finding
against the deliverable itself.

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | DA-NNN findings with severity |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | Prioritized action list |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |

---

## Summary

Six counter-arguments identified (4 Critical, 2 Major), all independently verified against the
ADR's own cited evidence corpus (`adr-convention-20260702-001` and `fu-log-convention-20260705-001`
iteration score reports and refutation-panel files). The ADR's central thesis -- that an
independent, criticality-proportional 3-lens refutation panel measurably improves tournament
scoring honesty -- is well-supported by the iteration 8-10 score-report data. However, direct
verification of the ADR's *own* supporting arithmetic surfaces a load-bearing, ironic defect: one
of the ADR's own cited cost-evidence numbers is factually false (DA-001), its cost-model formula
contradicts both its own constraint text and the underlying evidence (DA-002), its central
criticality-gating decision (D-1) is evidenced by zero C1/C2/C3 tournament rounds despite governing
all four criticality levels (DA-003), and its primary stated mitigation for the one risk this
review was specifically asked to probe (false-negative suppression via DEFAULT-REFUTED) describes
that mechanism's effect backwards (DA-004). Recommend **REVISE**: the six-decision architecture is
directionally sound and well-evidenced for its actual C4/ADR-genre sample, but the ADR overstates
the reach of that evidence (framework-wide, all-criticality, all-deliverable-type) and contains an
uncorrected factual error in its own quantitative self-support -- precisely the failure mode this
ADR exists to catch.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-20260707-i1 | ADR's own cited cost evidence is factually false: "18 verifier files" for fu-log iteration-8 vs. 12 actual | Critical | ADR lines 133, 626; actual directory has 12 files | Evidence Quality |
| DA-002-20260707-i1 | Cost-model formula contradicts its own constraint (c-004) and the empirical per-report bundling it cites as support | Critical | ADR lines 206, 624-626 vs. panel-file scope statements | Internal Consistency |
| DA-003-20260707-i1 | D-1's criticality-gating decision (C4/C3/C1-C2 split) is evidenced by zero C1, C2, or C3 tournament rounds -- 100% of the 18 cited rounds are C4 | Critical | ADR lines 246-266; `Criticality Level: C4` in every s-003/s-014 file across both packages | Methodological Rigor |
| DA-004-20260707-i1 | RSK-1's stated mitigation for false-negative risk misdescribes DEFAULT-REFUTED's own direction of effect | Critical | ADR line 707 vs. ADR's own D-1/D-2 definitions of DEFAULT-REFUTED (lines 381-382) | Internal Consistency |
| DA-005-20260707-i1 | n=2, single-genre (ADR/governance), single-pipeline evidence generalized to a permanent, framework-wide, all-criticality-level, all-deliverable-type change with no disclosed external-validity limitation | Major | ADR lines 79-85, 632-636, 703-712 (no such caveat in Risks or Consequences) | Completeness |
| DA-006-20260707-i1 | "Blind independence" (RSK-2's mitigation) is architectural/context independence only, not model/reasoning independence; the ADR's own fabricated-claim incident evidences a correlated model blind spot that context-separation alone does not rule out for the verifier panels | Major | ADR lines 168-176, 218-221, 708 | Methodological Rigor |

**Finding ID Format:** `DA-{NNN}-20260707-i1` (iteration 1, this blind execution).

---

## Finding Details

### DA-001: ADR's Own Cost-Evidence Citation Is Factually False [CRITICAL]

**Claim Challenged:** The ADR cites, twice, an empirical file count as support for its cost model:
(1) Context, line 133 (`.../fu-log .../iteration-008/`): "18 verification-panel files"; (2)
Constraints c-004, line 206: "iter-8 FU: 18 files."

**Counter-Argument:** This number is false. The actual directory
`projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/`
contains exactly **12** refutation-panel files, independently enumerated by this review (4
Critical-bearing reports -- S-001, S-002, S-004, S-012 -- x 3 lenses = 12), confirmed by two
independent glob passes. The ADR's own iteration-9 citation in the same sentence ("15 files = 3
lenses x 5") is internally correct (5 Critical-bearing reports x 3 lenses = 15, independently
confirmed by this review). Only the iteration-8 FU-log figure is wrong, and it is wrong by 50%
(18 claimed vs. 12 actual).

**Evidence:** Glob of `.../fu-log-convention-20260705-001/adversary/iteration-008/verify/*`
returns exactly 12 files (verified twice, including a broader `**/*refutation*` pattern to rule
out a missed subdirectory or casing variant). No 13th-18th file exists anywhere under that
iteration's `verify/` directory.

**Impact:** This is a direct, citable instance of exactly the failure mode the ADR's own headline
evidence chain warns against: an unverified quantitative claim, repeated twice as if authoritative,
that does not survive the one check that would have falsified it (counting the files). The ADR's
own iteration-10 evidence chain (lines 168-176) makes the identical point about a *different*
false claim ("no PR template exists -- Glob-verified") surviving four rounds uncaught -- this ADR
commits the same class of error in its own supporting arithmetic, uncaught through however many
authoring/self-review passes produced the final text.

**Dimension:** Evidence Quality

**Response Required:** Recount and correct the iteration-8 FU-log verifier-file figure at both
citing locations (Context line 133, Constraints c-004 line 206). Because a S-014 scoring pass
already exists for this deliverable, add a fact-check pass over every other cited quantitative claim
in the Context/Constraints sections before treating the corpus summary as settled.

**Acceptance Criteria:** Both citations corrected to 12 (or the corrected count from a fresh
recount); a note added disclosing the correction, consistent with the ADR's own subtraction/
disclosure doctrine (D-3) rather than a silent edit.

---

### DA-002: Cost-Model Formula Contradicts Its Own Constraint and Its Own Cited Evidence [CRITICAL]

**Claim Challenged:** Constraint c-004 (line 204): "The token cost of verification MUST be
proportionate to criticality (panels ~= 3 agent runs **per Critical-bearing report**)." L1
Technical Implementation "Cost model" (lines 624-626): "cost ~= **3 x (number of claimed
Criticals)** at C4, 3 x (Criticals) at C3, 0 at C1-C2. Empirically ~15-18 verifier files per C4
round."

**Counter-Argument:** These are two different units of work, and only one of them matches the
evidence the same paragraph cites as support. c-004 says the unit is the **report** (one
Critical-bearing strategy report gets 3 panel runs, regardless of how many Criticals that report
contains). The Cost model paragraph instead says the unit is the **individual claimed Critical**
(3 runs per claimed Critical). Applying the "3 x claimed Criticals" formula to the ADR's own cited
rounds: iteration 9 had **10** claimed Criticals (Panel-Outcome Reconciliation table, iter-9 score
report), so the formula predicts 30 files -- but only 15 exist (this review independently
confirmed 15, matching the ADR's own "15 files = 3 lenses x 5" aside, where "5" is 5 *reports*, not
5 Criticals). Iteration-8 FU-log had **7** claimed Criticals (Verification Roll-Up table), so the
formula predicts 21 files -- but only 12 exist (per DA-001). In both cases the empirical evidence
the ADR cites as support for its formula actually falsifies the formula by roughly 2x, because the
real, observed unit of verification work is the strategy **report** (which can bundle multiple
Criticals into one 3-lens pass, as confirmed directly in the panel files themselves -- e.g.
`iteration-009/verify/s-012 ... -refutation-materiality.md` states "Scope: All three Critical
findings in the target report (012-001, 012-002, 012-003)").

This also creates a genuine specification ambiguity for WI-1 (`adv-verifier`): the L1 Technical
Implementation's own invocation-contract sentence says "**one call per lens per Critical-bearing
report**" (report-level unit, matching c-004) in the same breath as "Input = **the single claimed
Critical** (id, severity, evidence, affected dimension)" (individual-finding-level unit, matching
neither c-004 nor the empirical practice for multi-Critical reports). An implementer following the
literal L1 text could build either a per-report verifier (2x cheaper, matches the evidence) or a
per-finding verifier (2x more expensive than what was ever empirically run) and the ADR's own text
would not tell them which is correct.

**Evidence:** ADR lines 204-206 (c-004), 624-626 (Cost model), 580-590 (invocation contract); iter-9
score report lines 19-38 (10 claimed Criticals); fu-log iter-8 score report lines 54, 63-71 (7
claimed Criticals, 6 VERIFIED + 1 REFUTED); independently-confirmed file counts (15 and 12
respectively, per DA-001).

**Impact:** The ADR presents a precise, load-bearing cost claim ("panels are ~3 agents per
Critical-bearing report" is the exact number the invoking task's own attack brief asked this review
to sanity-check) and gets the arithmetic wrong when the formula is read literally, while never
resolving which reading (per-report or per-finding) WI-1's implementer should build. Given that
token-cost proportionality is one of the ADR's six stated constraints (c-004) and one of its four
Alignment "HIGH" satisfaction claims, an implementation built to the literal "3 x claimed Criticals"
formula would cost roughly double what the cited evidence shows was actually incurred -- a material
difference at C4 scale.

**Dimension:** Internal Consistency (also Actionability: WI-1's acceptance criteria do not resolve
the ambiguity)

**Response Required:** Pick one unit of work (report-level, matching both c-004 and the empirical
practice, is the reading supported by the evidence) and make the L1 invocation contract, the Cost
model formula, and WI-1's acceptance criteria all state it identically and unambiguously.

**Acceptance Criteria:** A single, internally consistent cost formula appears in c-004, the Cost
model paragraph, and WI-1, phrased in terms of Critical-bearing *reports* (not individual claimed
Criticals), with the corrected iteration-8/iteration-9 file counts as its supporting arithmetic.

---

### DA-003: D-1's Criticality-Gating Decision Rests on Zero C1/C2/C3 Evidence [CRITICAL]

**Claim Challenged:** D-1 chooses Option C ("criticality-proportional verify: C4 all Criticals; C3
Criticals only; C1-C2 none") over Option B ("always-on verify... at every criticality"), reasoning
(line 264): "the spiral is an observed C4/C3-governance phenomenon over many rounds; C1-C2 work
(reversible in a day, <=10 files) neither exhibited it nor can afford ~3 agents per Critical."

**Counter-Argument:** This sentence claims C1-C2 work "neither exhibited" the spiral, framing the
C1-C2 exemption as evidence-led. It is not. Every single one of the 18 cited tournament rounds
across both packages is explicitly self-declared `Criticality Level: C4` -- independently confirmed
by this review via grep across every `s-003-findings.md` and `s-014-quality-score.md` file in both
`adr-convention-20260702-001` and `fu-log-convention-20260705-001` (36 matching lines, all reading
"C4"). There is no C1 round, no C2 round, and -- more importantly, since D-1's own gating table
prescribes a *different* panel policy for C3 ("Criticals only") than for C4 ("all Criticals") --
**no C3 round either**. The claim "C1-C2 work... neither exhibited it" is not a finding from the
record; it is an assumption about a criticality tier that was never run through the tournament at
all. The record cannot show an absence of a spiral in C1-C2 work, because no C1-C2 work is in the
record to check.

This also collapses the "always-on vs. conditional" question the review was specifically asked to
probe: at C4, Option C ("all Criticals get panels") and Option B ("every Critical gets panels,
always") are *identical* -- there is no criticality tier within the 100%-C4 evidence base where B
and C diverge. The empirical delta the ADR reports (0.68->0.86, 0.51->0.72, 0.68->0.88) is entirely
a "verification on vs. verification off" delta at C4; it is not evidence that criticality-*gating*
(as opposed to blanket always-on verification) is the right cut point, because the gate was never
exercised.

**Evidence:** ADR lines 246-266 (D-1 table and rationale); grep of `Criticality Level` across
`adr-convention-20260702-001/**` and `fu-log-convention-20260705-001/**` (36 matches, 100% "C4",
zero "C1"/"C2"/"C3" matches for either package's own tournament rounds).

**Impact:** D-1 is presented as "evidence-led" (c-005: "The decision must be evidence-led and cite
the tournament record") and scored HIGH on Constraint Satisfaction, but the specific C1-C2 vs. C3
vs. C4 cut points it prescribes are extrapolated, not observed. This does not mean the
extrapolation is wrong -- criticality-proportional cost gating is a reasonable design default -- but
the ADR's own rhetorical structure repeatedly claims the *whole* six-decision architecture is
evidence-led from an 18-round record, when the gating boundary itself (the one place D-1 actually
differs by criticality) is asserted, not measured.

**Dimension:** Methodological Rigor (also Evidence Quality)

**Response Required:** Either (a) relabel the C1-C2 exemption and the C3-vs-C4 split explicitly as
a reasoned default/extrapolation rather than an evidence-led finding, or (b) run at least one C2
and one C3 tournament round through both protocols (verified vs. unverified) before treating the
gating boundary as settled, consistent with the ADR's own subtraction/disclosure doctrine (state
what is inferred vs. what is measured, per P-022).

**Acceptance Criteria:** D-1's rationale paragraph explicitly distinguishes the measured claim (
"verification helps at C4, where 100% of the record lives") from the extrapolated claim ("this
generalizes to a C3-vs-C4 split and a C1-C2 exemption"), and c-005's "evidence-led" framing is
scoped accordingly.

---

### DA-004: RSK-1's Mitigation Misdescribes DEFAULT-REFUTED's Own Effect [CRITICAL]

**Claim Challenged:** Risk register, RSK-1 (line 707): "**Verifier leniency false-negative** -- a
real Critical is refuted and slips the gate. | MED | HIGH | **2-of-3 majority + DEFAULT-REFUTED
biases toward *keeping* claims**; factual lens is evidence-anchored (file+line); anti-leniency
mandate inherited from `adv-scorer.md:68-91`; convergence discriminator re-surfaces a genuinely
recurring defect in a later round."

**Counter-Argument:** This is the review's specific attack target ("does default-refuted risk
suppressing real findings -- and does the ADR honestly bound it?") and the answer is: no, the
stated mitigation is backwards. DEFAULT-REFUTED, by the ADR's own repeated definition (D-1 line
381: "2-of-3 majority, **DEFAULT-REFUTED**, blind to each other"; D-2 line 382: "Refuted claims
carry zero dimension weight"), means that when a lens is uncertain, it votes REFUTE, and a finding
must clear an affirmative 2-of-3 VERIFIED bar to count. This mechanism biases the *system* toward
**discarding** claims under uncertainty -- that is precisely the property that solves the
additive-remediation spiral (the false-*positive* problem: manufactured Criticals inflating the
count). It does not, and by construction cannot, simultaneously bias toward *keeping* claims; that
would require a DEFAULT-VERIFIED rule, the opposite policy. RSK-1 is exactly the mirror-image risk
(false *negative*: a real Critical wrongly discarded) that a discard-biased default necessarily
makes *more* likely, not less. Citing "DEFAULT-REFUTED... biases toward keeping claims" as RSK-1's
primary mitigation cites the very mechanism that creates RSK-1's exposure as if it were the cure.

The remaining mitigations in the same cell are weaker than they first appear once this is seen: "2-
of-3 majority" (as opposed to 3-of-3 unanimity) does make VERIFIED marginally easier to reach, which
is a genuine, if partial, counterweight -- but it is the *only* part of the cell that actually points
in the claimed direction, and the ADR does not disaggregate it from the incorrectly-described
DEFAULT-REFUTED claim. "Convergence discriminator re-surfaces a genuinely recurring defect in a
later round" (D-4) is also optimistic: it depends on a *different* blind strategy independently re-
deriving the same underlying issue in a subsequent round, which the record shows happening for one
specific recurring textual pattern (the grandfather-seam, independently re-derived by four
different strategy *types* in iteration 10) but is not established as a general property for
arbitrary refuted Criticals whose underlying text a different strategy family might simply never
probe the same way.

**Evidence:** ADR line 707 (RSK-1); ADR line 381 (D-1 decision definition of DEFAULT-REFUTED); ADR
line 382 (D-2: "Refuted claims carry zero dimension weight"); ADR lines 618-628 note the protocol
runs "one invocation per lens" but nowhere does the ADR reconcile "biases toward keeping claims"
with its own "DEFAULT-REFUTED" label.

**Impact:** This is the single highest-probability, highest-impact risk in the register (MED/HIGH,
the only such combination in the table), and it is the risk this review's invoking task explicitly
flagged as needing an honest bound. The stated primary mitigation does not logically hold up: it
describes DEFAULT-REFUTED's effect in the opposite direction from every other place in the same
document that defines the term. A reader relying on this cell to assess whether false-negative
risk is adequately bounded would be materially misled about the mechanism's actual behavior.

**Dimension:** Internal Consistency (also Methodological Rigor)

**Response Required:** Rewrite RSK-1's mitigation to state the true trade-off honestly: DEFAULT-
REFUTED necessarily trades some false-negative risk for its false-positive-suppression benefit; the
actual counterweights are (a) the 2-of-3-not-3-of-3 majority threshold (marginally pro-VERIFIED),
(b) the factual lens's evidence-anchoring (reduces, but does not eliminate, the chance an uncertain
lens votes REFUTE on a genuinely real finding), and (c) the convergence discriminator's *partial*,
not general, re-surfacing property. State explicitly that this is a deliberate, disclosed trade-off
(consistent with the ADR's own subtraction/honesty doctrine) rather than implying the mitigation
neutralizes the risk in both directions at once.

**Acceptance Criteria:** RSK-1's mitigation text no longer claims DEFAULT-REFUTED biases toward
"keeping" claims; the false-negative/false-positive trade-off inherent in any default-under-
uncertainty rule is named explicitly, with the residual false-negative exposure stated as a
disclosed, accepted risk rather than an eliminated one.

---

### DA-005: n=2, Single-Genre Evidence Generalized to a Framework-Wide, All-Criticality, All-Deliverable-Type Change [MAJOR]

**Claim Challenged:** L0 (line 79): "This ADR proposes to make that verification stage a permanent,
optional-by-criticality part of the `/adversary` tournament" -- i.e., the entire `/adversary`
skill, for all C3/C4 deliverables of any kind, framework-wide, not scoped to ADRs or governance
conventions.

**Counter-Argument:** The entire evidentiary record supporting this ADR consists of exactly two
artifacts, both ADRs/governance conventions (`ADR-PROJ031-004` + companion rule draft; the
feedback/decision-log design doc + staging files), both authored by the same agent role
(ps-architect / the same design-doc authoring pattern), both reviewed by the same fixed roster of
~9 finder strategies inside the same `/adversary` skill implementation, in the same project
(PROJ-031), over a period of days. This is not merely a small sample (n=2); it is a *maximally
correlated* sample -- every plausible confound (document genre, author, reviewer suite, time
period, skill version) is held constant across both instances rather than varied. Nothing in the
record speaks to whether the same effect holds for code review, security architecture review, API
contract review, or any non-ADR-genre C3/C4 deliverable that `/adversary` is also used for (per
`.context/rules/quality-enforcement.md` Criticality Levels, C3/C4 applies to "significant" and
"critical" decisions generally, not only to ADRs). Neither the Risks table (RSK-1 through RSK-6)
nor the Consequences section (Positive/Negative/Neutral) names this generalization gap anywhere;
the Neutral consequences note only that `ps-critic`/`/problem-solving` are out of scope (line
698-699), which is a different claim (scope of *this* ADR's blast radius) from external validity of
the *evidence* used to justify the in-scope decision.

**Evidence:** ADR lines 79-85 (L0, framework-wide framing), 108-112 (Context: both packages
described only as "2 C4 governance packages"), 663-698 (Consequences, no genre/external-validity
caveat), 703-712 (Risks, no genre/external-validity risk entry).

**Impact:** The six decisions (D-1 through D-6) may well generalize beyond ADR-genre documents, but
the ADR presents them as if the 18-round record already demonstrates this, when the record instead
demonstrates it for one narrow, internally-homogeneous case. A reader could reasonably expect the
verification stage to work identically well on, say, a security-architecture C4 review with very
different finding shapes (executable exploits vs. textual claim contradictions) -- an expectation
this ADR's own evidence does not support.

**Dimension:** Completeness (also Evidence Quality)

**Response Required:** Add an explicit limitation statement (Risks or Consequences) naming the
evidence base's genre/pipeline homogeneity and recommending a validation checkpoint (e.g., WI-8's
"dogfood on a sample deliverable," already proposed, could be explicitly required to include at
least one *non*-ADR-genre C3/C4 deliverable before the protocol is declared framework-wide-mature).

**Acceptance Criteria:** A named residual/risk entry disclosing the n=2/single-genre evidence base,
and a revised WI-8 acceptance criterion requiring validation against at least one non-ADR
deliverable type.

---

### DA-006: "Blind Independence" Conflates Context Isolation with Model/Reasoning Independence [MAJOR]

**Claim Challenged:** RSK-2 (line 708): "Lens collusion / non-independence... Mitigation:
Blindness enforced architecturally (separate T1 invocations, no shared context, no scorer
context)." Force 2 (line 218-221) similarly frames "blind independence" as the load-bearing
property.

**Counter-Argument:** Every finder, every lens, and the scorer are, per the ADR's own D-6 rationale
and this tournament's actual execution model, invocations of the same underlying reasoning system
under different prompts and context windows -- not independent human reviewers or differently-
trained models. "Blindness" here means context isolation (no shared state between invocations), not
diversity of the underlying reasoning process. These are different properties: context isolation
prevents one specific failure mode (a lens anchoring on another lens's stated verdict), but it does
not prevent a *correlated* failure mode where the same underlying model makes the same mistake in
every "independent" invocation because the mistake is a property of the model's own reasoning, not
of shared context. The ADR's own evidence contains a direct demonstration of exactly this: the
fabricated-verification incident (lines 170-176) -- the false "no PR template exists -- Glob-
verified" claim -- was independently re-asserted across iterations 6, 7, 8, and 9, each a nominally
separate, blind tournament pass (per the ADR's own framing, these were *not* colluding invocations
sharing context, yet all four converged on the identical wrong answer). If context-isolated
"blindness" were sufficient to guarantee independence, four separately-invoked passes converging on
the same false claim should be a low-probability event; instead it is exactly what happened, and it
took a fifth, differently-lensed pass (the factual-accuracy refutation lens) to catch it -- which is
itself evidence that the mechanism which eventually worked was a *different rubric/prompt*, not
"independence" in the ensemble-diversity sense the Risk register implies.

**Evidence:** ADR lines 168-176 (fabricated-verification incident, 4-iteration recurrence), 218-221
(Force 2, "blind independence"), 708 (RSK-2 mitigation).

**Impact:** This does not invalidate the verifier design -- a differently-prompted lens with a
distinct rubric plausibly does add real signal, as the PR-template catch demonstrates -- but the
Risk register's confidence that "blindness" (context separation) alone lowers collusion/non-
independence risk to LOW probability is not fully supported by the ADR's own cited incident, which
shows the opposite failure mode (correlated error surviving repeated "independent" passes) actually
occurring in this exact corpus. The mitigation conflates two distinct properties and may understate
RSK-2's true probability.

**Dimension:** Methodological Rigor (also Completeness)

**Response Required:** Distinguish, in RSK-2's mitigation text, between context-isolation
(architecturally guaranteed) and reasoning-diversity (not guaranteed by this design, since all
invocations share the same underlying model); consider naming the residual correlated-error risk
explicitly rather than folding it into "LOW probability."

**Acceptance Criteria:** RSK-2's mitigation names the context-isolation/reasoning-diversity
distinction explicitly and no longer implies context separation alone is sufficient evidence for
LOW collusion probability.

---

## Recommendations

**P0 (Critical -- MUST resolve before acceptance):**
- DA-001: Correct the false "18 files" citation (Context line 133, Constraints line 206) to the
  verified count (12). Add a disclosed-correction note.
- DA-002: Resolve the report-vs-finding cost-unit ambiguity across c-004, the Cost model paragraph,
  and WI-1's acceptance criteria; make the three internally consistent and evidence-matched.
- DA-003: Either relabel the C1-C2/C3-vs-C4 gating boundary as a reasoned default (not an
  evidence-led finding) or schedule a C2/C3 validation round before treating the boundary as
  settled.
- DA-004: Rewrite RSK-1's mitigation to describe DEFAULT-REFUTED's actual (discard-biased) effect
  and name the residual false-negative exposure honestly.

**P1 (Major -- SHOULD resolve; require justification if not):**
- DA-005: Add an explicit n=2/single-genre evidence-base limitation and require WI-8's validation
  pass to include a non-ADR-genre deliverable.
- DA-006: Distinguish context-isolation from reasoning-diversity in RSK-2's mitigation; name the
  residual correlated-error risk.

**P2 (Minor -- MAY resolve):** None identified at Minor severity in this pass; the leniency-bias
counteraction step (S-002 Step 3 decision point) was applied and did not surface findings below
Major severity that were not already subsumed into DA-001 through DA-006.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-005: framework-wide/all-criticality claim outruns the disclosed evidence scope; no genre-generalization limitation named. |
| Internal Consistency | 0.20 | Negative | DA-002 (cost-unit formula contradicts its own constraint), DA-004 (RSK-1 mitigation contradicts the ADR's own DEFAULT-REFUTED definition). |
| Methodological Rigor | 0.20 | Negative | DA-003 (criticality-gating boundary unevidenced at C1/C2/C3), DA-006 (context-isolation vs. reasoning-diversity conflated in risk analysis). |
| Evidence Quality | 0.15 | Negative | DA-001 (a specific, repeated quantitative claim is factually false and unverified against the cited primary source -- the exact failure class this ADR exists to catch). |
| Actionability | 0.15 | Negative | DA-002: WI-1's invocation contract is ambiguous between per-report and per-finding units, blocking a single unambiguous implementation. |
| Traceability | 0.10 | Neutral | Citations throughout the ADR are otherwise precise (file+line) and enabled this review's own verification; no traceability-specific finding surfaced. |

**Result:** 4 Critical and 2 Major findings identified. The six-decision architecture (D-1 through
D-6) is directionally well-supported by the C4/ADR-genre evidence it actually has, but the ADR
overstates that evidence's reach in three distinct ways (cost arithmetic, criticality-gating scope,
risk-mitigation direction) and is silent on a fourth (genre/deliverable-type generalization). Given
this ADR's own subject matter is "verify claims before counting them," the self-referential
character of DA-001 (an unverified false count in the ADR's own supporting evidence) and DA-004 (a
mitigation that misdescribes its own mechanism) are the two highest-priority items for revision.

---

*Constitutional compliance: P-003 (no subagents invoked); P-020 (writes confined to
`projects/PROJ-031-cowork-skeleton/`; the deliverable itself was not edited); P-022 (all findings
cite file+line or independently-reproduced file counts; DA-005 and DA-006 are labeled as reasoned
inference rather than direct textual contradiction). All paths in this report are repo-relative; no
absolute filesystem paths or employer-internal tokens are present.*
