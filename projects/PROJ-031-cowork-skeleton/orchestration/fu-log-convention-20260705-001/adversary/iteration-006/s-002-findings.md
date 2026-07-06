# Devil's Advocate Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention Package (Iteration 6)

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverable, H-16 compliance |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | DA-NNN identifiers, severity, evidence |
| [Finding Details](#finding-details) | Full analysis of Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Execution Context

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md,FEEDBACK-LOG.template.md,LLM-DECISION-LOG.template.md,examples-appendix.md,hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (iteration 6, blind protocol — no read of sibling strategy findings)
**H-16 Compliance:** S-003 Steelman output file confirmed present at `.../adversary/iteration-006/s-003-findings.md` (existence verified via directory listing per blind protocol; content NOT read, consistent with the blind-agent isolation instruction). Ordering constraint satisfied procedurally by the 6-group sequential orchestration (self-refine → steelman → challenge → ...).

**Attack brief (as assigned):** (1) does segment rotation solve the log-growth problem or just shard it (index growth, cross-segment search burden)? (2) does the alias/canonical-id split create ambiguity when the user references "FU.1" from three turns ago? (3) is the convention adoptable by users other than the current single operator? Package is explicitly MEDIUM-tier/minimal by convention; descoped-with-disclosure is accepted; overclaimed coverage is classified Critical per assignment instructions.

---

## Summary

4 counter-arguments identified (1 Critical, 2 Major, 1 Minor). The package's core mechanisms (segment rotation, logger-assigned canonical ids + verbatim aliases) are honestly disclosed as bounded/partial in most places, and prior iterations (1-5, visible only as file listings under the blind protocol) have already forced multiple disclosure fixes on these exact topics. This iteration's findings target narrower, still-open gaps that survive those fixes: (a) the document's own "named as such" correlated-risk enumeration under-counts a fifth instance of the same shared-checkpoint dependency, one that is itself part of the segment-rotation growth-mitigation chain (DA-001, Critical — an overclaim-of-coverage per the assignment's explicit criterion); (b) the alias scheme's "zero maintenance burden" framing does not address the unbounded read-time back-reference disambiguation cost, and the H-31 enumeration protocol has no described mechanism to use the user's own disambiguating context to narrow candidates (DA-002, Major); (c) the "untested for a different operator" residual — unlike every sibling residual in this package — carries no re-assessment trigger or forcing function despite the artifact being routed toward framework-wide install (DA-003, Major); (d) the appendix's only worked disambiguation example under-represents the candidate-list size a long, faithfully-followed session would actually produce (DA-004, Minor). Recommend **targeted revision** (wording/propagation-class fixes only, no new machinery) addressing DA-001 through DA-003 before this package proceeds toward the 0.95 gate.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter6-20260706 | "Four safety functions" correlated-risk enumeration under-counts a fifth instance (segment-index overflow re-assessment) that shares the same commit-cadence-checkpoint SPOF and is itself the growth-mitigation's own escape hatch — an overclaim of disclosure completeness | Critical | `design/feedback-decision-log-convention-design.md:184,241,248` | Internal Consistency |
| DA-002-iter6-20260706 | Alias scheme's "zero maintenance burden" claim addresses write-time cost only; read-time H-31 back-reference disambiguation cost is unbounded and the enumeration protocol has no described mechanism to use user-supplied temporal context ("three turns ago") to narrow candidates | Major | `design/feedback-decision-log-convention-design.md:70,72-73,198`; `FEEDBACK-LOG.md:113-121` | Completeness |
| DA-003-iter6-20260706 | "Untested for a different operator" residual has no re-assessment trigger/forcing function unlike every sibling residual (Q1-Q5, Q3 hook, segment index), despite the artifact being routed to framework-wide install where every new operator is an uninstrumented live test of that claim | Major | `design/feedback-decision-log-convention-design.md:99,236-238,241`; `design/staging-feedback-logs/feedback-decision-logs-standards.md:59` | Methodological Rigor |
| DA-004-iter6-20260706 | The only worked disambiguation example (appendix "Common cases") shows a 3-4-candidate list; no example demonstrates the realistic N>3 case a long session following the design's own target operator habit (restart every turn) would produce | Minor | `design/staging-feedback-logs/examples-appendix.md:169` | Evidence Quality |

**Finding ID Format:** `DA-{NNN}-iter6-20260706` (iteration 6, this execution).

---

## Finding Details

### DA-001: Segment-Index Overflow Is the Growth Problem's Own Unremediated Escape Hatch, and the Document Under-Counts It [CRITICAL]

**Claim Challenged:** `design/feedback-decision-log-convention-design.md:248` — "**One shared dependency, named as such (accepted correlated risk, RT-003/PM-002).** Four safety functions — staleness review, graduation proposal, Backfill-Queue review, and this install-stall re-assessment — all fire at the **same** commit-cadence checkpoint... The correlation is **accepted, not papered over with new machinery**."

**Counter-Argument:** The claim to have exhaustively "named" every function sharing the correlated commit-cadence-checkpoint SPOF is itself incomplete. `design/feedback-decision-log-convention-design.md:184` states the Segment Index's own overflow mitigation — the mechanism that keeps the FU.5 growth-solving promise from degrading into "index rows crowd out entries" — **also** fires "at the same commit-cadence checkpoint used elsewhere": *"if one ACTIVE segment's index+queue overhead ever exceeds ~100 lines, revisit at the **same commit-cadence checkpoint used elsewhere** — the fallback is to move the Segment Index to its own `*-INDEX.md` sidecar (deferred to that future revision; not built now)."* That is a fifth function riding the identical SPOF, uncounted in the "Four safety functions" list. This directly answers the assigned attack ("does segment rotation solve the growth problem or just shard it — index growth?"): the growth problem is not solved, it is deferred into the segment index, and the index's own overflow safeguard is (a) informal (a "revisit" with no forcing function, unlike the Q3 hook's forcing function at line 241 — *"at install, this Q3 re-assessment is recorded as a **dated worktracker item**... so the sole compensating control... has an accountable owner and a review date, not only narrative triggers"*), and (b) not even propagated into the shipped rule file (`design/staging-feedback-logs/feedback-decision-logs-standards.md` LOG-M-006, lines 27-28, describes the entry-count/line-count cap and the near-cap `grep -c` id-derivation trick, but contains no mention of the ~100-line index-overflow trigger at all — an installer reading only the shipped artifact has zero visibility into this residual). Improvement Ledger row 9 (`design/feedback-decision-log-convention-design.md:266`) already concedes segment rotation "bounds single-read size, not total-corpus search" — but does not concede that the index itself is an unbounded-growth structure sharing the very capacity budget (the ~800-line cap) it exists to protect.

**Evidence:** `design/feedback-decision-log-convention-design.md:184` (segment-index overflow + informal re-assessment trigger), `:241` (PM-005 forcing-function precedent, for contrast), `:248` (the under-counted "Four safety functions" claim), `:266` (Ledger row 9's own "not total-corpus search" concession); `design/staging-feedback-logs/feedback-decision-logs-standards.md:27-28` (LOG-M-006, no index-overflow trigger present in the shipped rule).

**Impact:** The package's central P-022 disclosure posture ("named as such, not papered over") is undermined by its own miscount on the exact mechanism (segment rotation) that is this attack's subject. Per the assignment's explicit instruction, an overclaim of disclosure/coverage completeness is classified Critical.

**Dimension:** Internal Consistency (primary); Completeness (secondary — the shipped rule file omits the residual entirely).

**Response Required:** (a) Add the segment-index-overflow re-assessment as the fifth item in the "Four safety functions" enumeration (rename to "five," one line); (b) either give it the same forcing-function treatment as Q3 (a dated, owned worktracker trigger) or explicitly state why it is exempt; (c) propagate the ~100-line trigger (or at minimum a pointer to the design doc) into the shipped `feedback-decision-logs-standards.md` LOG-M-006 text so an installer who never reads the design doc still sees the residual.

**Acceptance Criteria:** The "shared dependency" count and the shipped rule file text are both updated; no new lint, file, or subsystem is introduced (consistent with the anti-bloat doctrine already governing every other fix in this package's changelog).

### DA-002: "Zero Maintenance Burden" Does Not Address the Unbounded Read-Time Disambiguation Cost, and H-31 Enumeration Ignores Available Disambiguating Context [MAJOR]

**Claim Challenged:** `design/feedback-decision-log-convention-design.md:70` — "Aliases may repeat and restart freely... they carry **zero maintenance burden**."

**Counter-Argument:** "Zero maintenance burden" is true only for the write-time cost (the operator never tracks a counter) — it is silent on the read-time cost the same paragraph's sibling clauses concede exists: `:72-73` states a bare back-reference is ambiguous because "the same token maps to several ids across turns," requiring the assistant to "enumerate the candidates and ask which one is meant," and that this enumeration "degrades to a multi-segment heading scan once rotation has occurred" (`:198`). The specific attack scenario assigned — a user referencing "FU.1" from three turns ago — is the worst case for this exact mechanism: the design's own target operator habit (FEEDBACK-LOG.md:113-121, FU.6: *"Typically I re-start at FU.0. everytime a turn happens... I also start from FU.0. in every document"*) means that the more faithfully the operator follows the very habit this scheme was built to accommodate, the more turns will contain an alias `FU.1`, and the longer the candidate list becomes at the exact moment disambiguation is needed. Neither the design doc nor the shipped templates describe the H-31 enumeration protocol using the user's own disambiguating language (e.g., "three turns ago," a topic keyword, or a session boundary) to narrow the candidate set before presenting it — the protocol as documented is "enumerate all matches, then ask," not "use available context to filter, then ask only if still ambiguous." This is a completeness gap in an already-disclosed mechanism, not a novel discovery of the ambiguity itself (which the design already discloses) — the specific gap is that the mitigation stops at "ask the user" without first exploiting information already present in the user's own query.

**Evidence:** `design/feedback-decision-log-convention-design.md:70` ("zero maintenance burden"), `:72-73` (H-31 back-reference enumeration + "both axes"), `:198` (multi-segment degradation); `FEEDBACK-LOG.md:113-121` (FU.6 verbatim, the restart-every-turn habit this scheme is built around); `design/staging-feedback-logs/examples-appendix.md:169` (the sole worked example of the enumeration, which does not demonstrate context-narrowing).

**Impact:** A reader of the "zero maintenance burden" framing in isolation could reasonably conclude the id/alias split is costless; the actual trade is a cost shift from write-time (eliminated) to read-time (potentially large, and currently un-narrowed by available context). At C4/engagement-gate-0.95 rigor, this framing gap is a Completeness/Evidence-Quality risk, not merely a style nit.

**Dimension:** Completeness.

**Response Required:** Either (a) add a one-clause hedge next to the "zero maintenance burden" claim noting the burden shifts to read-time disambiguation (already partially true elsewhere in the doc — this is a propagation fix, the same SM-003 class of fix this package has repeatedly applied), and/or (b) add one sentence to the H-31 enumeration procedure instructing the assistant to use user-supplied temporal/topical cues to narrow or rank candidates before presenting the full list.

**Acceptance Criteria:** No new machinery; a propagation-class wording fix consistent with the rest of this package's remediation history.

### DA-003: The "Untested for a Different Operator" Residual Is the Only Disclosed Risk in This Package With No Re-Assessment Trigger, Despite Being Routed to Framework-Wide Install [MAJOR]

**Claim Challenged:** `design/feedback-decision-log-convention-design.md:99` — "The id/alias scheme is validated against *this* project's single operator only; whether it transfers to a different operator's labeling habit is untested `[INFERENCE]`, not a claim." Also present verbatim in the shipped rule file: `design/staging-feedback-logs/feedback-decision-logs-standards.md:59`.

**Counter-Argument:** This disclosure is honest and adequately hedged as far as it goes — it is not, on its own, an overclaim (prior iterations already forced its addition, per the changelog's DA-005/DA-001 entries at iterations 3 and 4). The gap this iteration surfaces is procedural, not rhetorical: every other open residual in this package that the design doc itself flags as consequential gets an explicit re-assessment mechanism with a trigger and, in the Q3 case, an owner and a dated worktracker item (`:241`, PM-005: *"so the sole compensating control for MEDIUM-tier capture has an accountable owner and a review date, not only narrative triggers"*). The "untested for a different operator" residual gets none of this — it is a static, permanent disclosure with no plan to convert "untested" into "tested" (e.g., no criterion such as "re-assess after N distinct operators have used this convention," no feedback-capture mechanism for a second operator's friction). This matters specifically because the Adoption/migration plan (`:236-238`, steps 1-3) routes this artifact toward install into `.context/rules/` — a framework-wide location that, by construction, will be exercised by every future Jerry session on every future project. The moment this rule is installed, every subsequent operator who is not the current one becomes a live, uninstrumented test of the exact claim the design labels "untested" — yet no step in the Adoption plan gates on, or even mentions, gathering that evidence. Team/multi-writer use is explicitly called out as an out-of-scope extension (`:99`) with a stated rationale (no coordination machinery for an unstated requirement) — but a *different single operator* adopting the same convention on a different project is a materially different, much more likely near-term scenario than a multi-writer team, and it receives no comparable scoping treatment.

**Evidence:** `design/feedback-decision-log-convention-design.md:99` (the untested-for-different-operator disclosure), `:236-238` (Adoption plan steps 1-3, no adoptability-validation gate), `:241` (the PM-005 forcing-function pattern this residual lacks); `design/staging-feedback-logs/feedback-decision-logs-standards.md:59` (same disclosure, shipped, still no trigger).

**Impact:** Not a defect in the disclosure itself (which is honest and correctly hedged), but a consistency gap in how rigorously this package treats its own residuals — and the one residual singled out for lighter treatment is the one most directly implicated by the "adoptable by other users" question this attack was assigned to probe.

**Dimension:** Methodological Rigor (uneven application of the package's own forcing-function standard); Traceability (no owner/trigger to follow up on).

**Response Required:** Add a one-line re-assessment trigger for the operator-transferability claim (e.g., "revisit after this convention has been used, unmodified, by a second distinct operator on a second project — capture their friction as a Backfill/FEEDBACK-LOG entry against this convention itself") — reusing existing machinery (the very FEEDBACK-LOG this package ships) rather than adding anything new.

**Acceptance Criteria:** A dated or milestone-bound trigger exists for the operator-transferability residual, symmetric with the Q3/graduation/backfill triggers already in the document; zero new subsystems.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- **DA-001:** Correct the "Four safety functions" count to five (add the segment-index-overflow re-assessment); give it a forcing function or an explicit documented exemption; propagate the ~100-line index-overflow trigger (or a pointer to it) into the shipped `feedback-decision-logs-standards.md` LOG-M-006 text.

**P1 (Major — SHOULD resolve; justify if not):**
- **DA-002:** Add a one-clause read-time-cost hedge beside the "zero maintenance burden" claim; add one instruction to the H-31 enumeration procedure to use user-supplied context (temporal/topical) to narrow candidates before presenting the full list.
- **DA-003:** Add a re-assessment trigger for the "untested for a different operator" residual, reusing the FEEDBACK-LOG itself as the capture mechanism for a second operator's friction.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- **DA-004:** Add one additional worked example (or a sentence) to `examples-appendix.md`'s "Common cases" section illustrating a larger (N>3) candidate list under sustained restart-every-turn use, so reviewers can see the realistic degraded case, not only the 3-4-candidate illustration currently shown.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-002: read-time disambiguation cost and context-narrowing gap left undisclosed at the point of the "zero burden" claim. |
| Internal Consistency | 0.20 | Negative | DA-001: the "Four safety functions... named as such" claim under-counts a fifth instance of its own subject matter. |
| Methodological Rigor | 0.20 | Negative | DA-003: forcing-function standard applied to Q3/graduation/backfill but not to the operator-transferability residual. |
| Evidence Quality | 0.15 | Negative | DA-004: sole worked disambiguation example does not represent realistic scale. |
| Actionability | 0.15 | Neutral | All findings have concrete, single-line, no-new-machinery fixes (already demonstrated feasible by this package's own remediation history). |
| Traceability | 0.10 | Negative | DA-003: no owner/date exists for the operator-transferability residual, unlike its siblings. |

**Result:** 1 Critical, 2 Major, 1 Minor. All four findings are closeable by wording/propagation-class edits consistent with this package's established anti-bloat remediation pattern (no new lint, file, or subsystem required for any of them). Recommend **targeted revision** addressing DA-001 (P0) and DA-002/DA-003 (P1) before re-scoring against the 0.95 gate.
