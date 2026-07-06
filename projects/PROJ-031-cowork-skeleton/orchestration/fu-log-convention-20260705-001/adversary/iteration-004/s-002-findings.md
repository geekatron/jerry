# Devil's Advocate Report: FU-Log Convention Package (Iteration 4)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-002, iteration 4, blind protocol)
**H-16 Compliance:** See [H-16 Compliance Note](#h-16-compliance-note) — status: UNVERIFIED-BY-DESIGN (see note), not a violation finding against the deliverable itself.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [H-16 Compliance Note](#h-16-compliance-note) | Steelman-before-critique ordering status under blind protocol |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All DA-NNN findings |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 action list |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |

---

## H-16 Compliance Note

This invocation did not include a "Prior Strategy Outputs" field, and the BLIND PROTOCOL for this execution explicitly forbids reading any file under `orchestration/fu-log-convention-20260705-001/adversary/` other than this executor's own output file — which prevents direct verification of an S-003 (Steelman) output for this iteration. Per the user's established multi-group blind-agent convention (self-refine → steelman → challenge → verify → decompose → score, run sequentially between groups / parallel within), S-003 is expected to have executed in the "steelman" group prior to this "challenge" group (S-002) within iteration 4. This executor could not confirm that directly without violating the blind protocol designed to prevent cross-agent bias, and is flagging this as a **process note for the orchestrator to confirm**, not as a finding against the deliverable's content. Execution proceeded on the (labeled) **[INFERENCE]** that H-16 ordering was satisfied at the orchestration layer.

---

## Summary

6 counter-arguments identified (1 Critical, 3 Major, 2 Minor) against a deliverable package that has already survived three prior remediation rounds (0.66 → 0.65 → 0.59, per the design doc's own Revision Changelog) targeting overclaim language specifically. This pass targets the three assigned attack vectors and finds: (1) segment rotation solves the single-Read-window overflow problem the user actually asked for, but its own bookkeeping (the Segment Index) is rate-bounded, not size-bounded, and the design's word choice ("bounded") outruns what its own math shows; (2) the alias/canonical-id ambiguity attack is not hypothetical — a real collision (canonical `FU.1` vs. alias `FU.1` at `FU.9`) already exists in the live bootstrap `FEEDBACK-LOG.md` slated for adoption, and the disambiguation mechanism has never been exercised against it; (3) the "adoptable by other users" claim rests on an un-hedged generalization ("the id scheme generalizes cleanly to any other single operator's alias habit") stated as fact, with no [INFERENCE] label, in a document that is otherwise scrupulous about labeling inferences — this is the overclaim the task brief specifically flags as Critical. None of these findings require new machinery to close; all are wording, disclosure, or user-confirmation fixes consistent with the anti-bloat remediation pattern already used in iterations 1–3. Recommend REVISE (targeted, not structural).

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-i4 | "Generalizes cleanly to any other single operator" is an un-hedged, unvalidated generalization claim | **Critical** | `design/feedback-decision-log-convention-design.md:97` | Evidence Quality / Internal Consistency |
| DA-002-i4 | Real, live alias/canonical `FU.1` collision already exists in the bootstrap log; disambiguation mechanism untested against it | Major | `FEEDBACK-LOG.md:41` (canonical FU.1) vs. `FEEDBACK-LOG.md:148` (alias FU.1 at FU.9) | Methodological Rigor / Evidence Quality |
| DA-003-i4 | Segment Index growth is rate-bounded, not size-bounded; "bounded" wording outruns the design's own math, and no failure-mode is defined at the point the index consumes the entry budget | Major | `design/feedback-decision-log-convention-design.md:182` | Completeness / Evidence Quality |
| DA-004-i4 | FU.5 verbatim ("navigate forward and backwards between the decision and feedback logs") is ambiguous between cross-log linked traversal and per-log segment linking; the design silently picked the weaker (per-log) reading without flagging it for P-020 confirmation | Major | `FEEDBACK-LOG.md:107` vs. `design/.../convention-design.md:183` | Traceability / Completeness |
| DA-005-i4 | Operational file-count growth from rotation (dozens/hundreds of sealed `.NNN.md` files at scale) is undisclosed | Minor | `design/.../convention-design.md:178-183` (no count-of-files disclosure) | Completeness |
| DA-006-i4 | Alias-field overhead (`(alias: —)` boilerplate + back-reference protocol) is installed framework-wide for every Jerry adopter to accommodate one documented operator's specific habit | Minor | `FEEDBACK-LOG.md:118` (FU.6 verbatim) vs. staged install target `.context/rules/`, `.context/templates/` | Actionability |

**Finding ID Format:** `DA-{NNN}-i4` (execution_id = iteration 4, this tournament run).

---

## Finding Details

### DA-001-i4: Unvalidated "generalizes cleanly" claim [CRITICAL]

**Claim Challenged:** `design/feedback-decision-log-convention-design.md:97` — "**Team / multi-writer adoption is an explicit out-of-scope extension** — the id scheme generalizes cleanly to any *other single* operator's alias habit, but a multi-writer project would need a coordination rule beyond the current post-hoc lint; that machinery is deliberately not built for an unstated requirement."

**Counter-Argument:** The document has an established, consistently-applied convention of explicitly labeling unverified claims as `[INFERENCE]` (e.g., `design/.../convention-design.md:121` — "`[INFERENCE]`: no transcript-retention policy is cited"; `hook-design-note.md:29` — "`[INFERENCE]`: model is not on hook stdin"). The claim that the id/alias scheme "generalizes cleanly to any other single operator's alias habit" receives no such label, despite being exactly the kind of claim the document elsewhere is careful to hedge: it is a universal ("any") claim about behavior for operators whose habits have never been observed, tested, or even hypothesized about beyond "some other single operator." The entire alias mechanism (canonical/alias split, back-reference H-31 enumeration, the appendix worked examples) was purpose-built around one specific, quoted operator habit — "Typically I re-start at FU.0. everytime a turn happens… I also start from FU.0. in every document that I am reviewing" (`FEEDBACK-LOG.md:118`, FU.6 verbatim). No evidence is offered that the scheme handles, for example, an operator who never labels items at all beyond the already-covered `alias: —` default, an operator who uses their OWN monotonic scheme that could itself collide lexically with canonical `FU.N` syntax, or a team context where "single operator" assumptions (already flagged out-of-scope) blur at the edges (e.g., one human operator working with two different assistant sessions in parallel, which is a single-operator, non-team scenario the design does not evaluate against the "generalizes cleanly" claim). This is precisely the class of finding the task brief calls out: **overclaimed coverage is Critical**, distinct from the many properly-hedged disclosures elsewhere in the same document (the "descoped-with-disclosure" posture is otherwise well executed — see the extensive, honest Revision Changelog at `.../convention-design.md:318-320`).

**Evidence:** `design/feedback-decision-log-convention-design.md:97`; contrast with the labeling convention at `design/feedback-decision-log-convention-design.md:121` and `design/staging-feedback-logs/hook-design-note.md:29`; root habit basis at `FEEDBACK-LOG.md:118`.

**Impact:** If this package installs to `.context/rules/` and `.context/templates/` (staged target per `design/.../convention-design.md:304-308`), every future Jerry project/operator inherits a scheme whose generalizability claim is asserted, not demonstrated. A future operator whose habits differ materially could experience friction (or outright confusion, per DA-002) that this document currently represents as a solved, universal case.

**Dimension:** Evidence Quality (0.15) primary; Internal Consistency (0.20) secondary (the document's own inference-labeling discipline is inconsistently applied).

**Response Required:** Either (a) re-label the claim as `[INFERENCE]` and narrow it to "generalizes to operators who exhibit a similar restart-and-relabel habit; untested against other patterns," or (b) provide at least one concrete alternative-operator scenario worked through to demonstrate the "cleanly" claim, consistent with the existing worked-example convention (`examples-appendix.md`).

**Acceptance Criteria:** The word "cleanly" and the scope word "any" are either removed/hedged, or backed by a second worked scenario. No new lint or mechanism required — this is a wording fix, consistent with the anti-bloat remediation pattern already used three times in this same package's history.

---

### DA-002-i4: Real alias/canonical collision already present in the adopted bootstrap log [MAJOR]

**Claim Challenged:** `design/feedback-decision-log-convention-design.md` L1.1 (Id scheme) — "Back-reference disambiguation (H-31)... The assistant enumerates the candidates and asks which one is meant (per H-31), rather than silently inferring from recency."

**Counter-Argument:** This mitigation is asserted but not validated against a collision that already exists, right now, in the artifact this same package's Adoption plan explicitly proposes to adopt in place (`design/.../convention-design.md:235`, Adoption step 4: "Adopt the two bootstrap files in place... entries and ids are preserved"). Specifically:
- Canonical `FU.1` = "subtraction-authorization" (`FEEDBACK-LOG.md:41`), disposition **IN-PROGRESS** ("gate NOT met after 8 total rounds; protocol decision escalated to user").
- A separate entry, `FU.9` = "skills-adversary-usage" (`FEEDBACK-LOG.md:148`), carries **user label: FU.1** (i.e., its alias is `FU.1`), disposition also **IN-PROGRESS**.

If the user (or a future session) asks "what's the status of FU.1?" today, per the design's own back-reference rule this bare token must be enumerated on both axes — the live canonical `FU.1` and the alias-matching `FU.9` — and both currently share the same disposition value (`IN-PROGRESS`), meaning even a correctly-enumerated candidate list does not let the user distinguish without reading full entry content. This is the exact scenario named in the attack brief ("does the alias/canonical-id split create ambiguity when the user references 'FU.1' from three turns ago?") — and the answer, demonstrated with the package's own data, is yes. Notably, the worked disambiguation example the design ships (`examples-appendix.md:24-32`) uses a **synthetic** three-way `FU.0` collision rather than the real `FU.1` collision already sitting in the file being adopted — so the mechanism has been illustrated, but not exercised against the actual case.

**Evidence:** `FEEDBACK-LOG.md:41` (canonical FU.1 heading and IN-PROGRESS disposition); `FEEDBACK-LOG.md:148` ("### FU.9 skills-adversary-usage (user label: FU.1)"); `design/staging-feedback-logs/examples-appendix.md:24-32` (synthetic FU.0 worked example, not the real FU.1 case); design rule at `design/.../convention-design.md` L1.1 "Back-reference disambiguation (H-31)" paragraph.

**Impact:** The disambiguation mechanism may work correctly if followed to the letter, but its untested status against a real, already-existing case in the very file slated for adoption is a methodological rigor gap at C4/0.95-gate stakes: a claim this load-bearing (it is the sole mitigation for the entire alias-ambiguity risk class) should be demonstrated against real data before the package is accepted, not asserted and left for the first live user query to discover.

**Dimension:** Methodological Rigor (0.20) primary; Evidence Quality (0.15) secondary.

**Response Required:** Add a one-line worked-example update (or a footnote) in `examples-appendix.md` demonstrating the disambiguation walkthrough against the *actual* `FU.1` collision already present in `FEEDBACK-LOG.md`, showing the two-candidate enumeration and how a user would distinguish them (likely: quoting each entry's slug/summary in the enumeration, not just the id).

**Acceptance Criteria:** No new lint or subsystem — a documentation/example update using data the package already contains. This closes the "untested claim" gap without adding machinery.

---

### DA-003-i4: Segment Index growth is rate-bounded, not size-bounded [MAJOR]

**Claim Challenged:** `design/feedback-decision-log-convention-design.md:182` (Segment index row) — "**Index growth is bounded to ≈1 row / 50 entries**: a 10k-entry log yields ~200 rows (~200 lines)."

**Counter-Argument:** "Bounded" is the wrong word for what the design's own math describes: a linear growth **rate** (1 row per 50 entries), not an absolute ceiling. The very next clause proves this: "at that scale a segment seals at ~40 (not ~50) entries" — i.e., as total corpus size N grows, the Segment Index (which lives only in the ACTIVE file and shares its 800-line cap with actual entries) consumes a growing absolute share of that cap, shrinking the effective entry-capacity of every subsequent segment. This is precisely the "shards, doesn't solve" pattern the attack brief asks about: single-Read-window overflow is genuinely solved (the user's stated problem), but the design's own bookkeeping reproduces a smaller-scale version of the same unbounded-growth problem it was built to prevent, and at sufficiently large N (the design's own extrapolation: "revisit if... overhead ever exceeds ~100 lines"), the mechanism's own math implies each new segment could seal at a handful of entries — or, taken to the extreme the design does not walk through, a scenario where the Index alone approaches the 800-line cap and no room remains for any entries in that segment. The "Re-assessment trigger" is a promise to *revisit*, not a defined fallback; there is no described behavior for what happens if/when that trigger fires.

**Evidence:** `design/feedback-decision-log-convention-design.md:182` (full Segment index row, "Index growth is bounded..." through "Re-assessment trigger... not open-ended").

**Impact:** For a long-lived project (the exact scenario FU.5 was raised to address — "long running sessions and or projects," `FEEDBACK-LOG.md:104`), the mechanism degrades gracefully for a long time but has no defined terminal behavior. This does not invalidate the core design (which correctly solves the stated read-window problem) but the word "bounded" overstates what is actually a favorable-but-still-growing ratio, and the corpus-search cost is a separate, honestly disclosed trade (L1.4 "Discovery-cost boundary") that this finding does not dispute.

**Dimension:** Completeness (0.20) primary; Evidence Quality (0.15) secondary (word choice outruns the math shown in the same sentence).

**Response Required:** Reword "Index growth is bounded to ≈1 row / 50 entries" to something like "Index growth is rate-limited to ≈1 row / 50 entries (not size-bounded — see re-assessment trigger)," and state explicitly what the re-assessment trigger's fallback behavior is expected to be (even if the answer is simply "defer to a future design revision at that point" — that is an acceptable anti-bloat answer, but it should be stated rather than left implicit).

**Acceptance Criteria:** Wording fix + one sentence naming the (even if deferred) fallback. No new machinery required.

---

### DA-004-i4: Silently-resolved ambiguity in the FU.5 "linked-list between logs" requirement [MAJOR]

**Claim Challenged:** User verbatim, `FEEDBACK-LOG.md:107` (FU.5) — "We should probably treat this like a linked-list so that it's easy to navigate forward and backwards **between the decision and feedback logs**."

**Counter-Argument:** This phrase is genuinely ambiguous between two readings: (a) "treat *each* of the two logs [decision log and feedback log] as its own linked-list of segments" (the reading the design implements), or (b) "make it possible to navigate forward/backward *between* the decision log and the feedback log [i.e., a literal cross-log linked traversal]." The design implements reading (a) as **prev/next segment headers, intra-log only** (`design/.../convention-design.md:183`, "Linked-list (bidirectional): each file's header blockquote carries `Segment N · prev · next`"), and separately implements a *different, weaker* mechanism for cross-log reference: ad-hoc canonical-id citation ("Cross-log navigation... achieved purely by canonical id... No file paths in cross-references, no extra machinery"). Citation-by-id is not a linked-list (no prev/next, no traversal order, no way to walk "the next decision after this feedback item" without already knowing which id to look up) — it is a weaker mechanism than what reading (b) would require. The design silently adopted the weaker, easier-to-build reading without flagging the ambiguity or asking the user to confirm which was meant, despite the rest of the package being disciplined about routing genuinely open questions to explicit P-020 ratification (Q1–Q4, `design/.../convention-design.md:265-276`). This is exactly the kind of interpretation choice H-31 ("clarify when ambiguous... MUST ask when multiple interpretations exist") calls out.

**Evidence:** `FEEDBACK-LOG.md:107` (FU.5 verbatim, "between the decision and feedback logs"); `design/feedback-decision-log-convention-design.md:183` (Linked-list row, intra-log prev/next) vs. the same table's "Cross-log navigation" row (id-citation only, no traversal).

**Impact:** If the user's actual intent was reading (b), the shipped design under-delivers on a load-bearing FU.5 requirement without ever surfacing that gap for confirmation — the exact failure mode (silent scope narrowing on a user-facing requirement) that this project's own prior incident (the ADR-convention over-engineering spiral, cited repeatedly in this package as the cautionary precedent) was not about, but which is the opposite-direction risk: under-scoping without disclosure, rather than over-building.

**Dimension:** Traceability (0.10) primary; Completeness (0.20) secondary.

**Response Required:** Add one line to the FU.5 disposition (or the L1.4 section) explicitly confirming with the user which reading was intended, alongside the existing PROPOSED-DEFAULT pattern already used for Q1–Q4 — this is a natural fifth confirmation item, not a new mechanism.

**Acceptance Criteria:** A one-line disclosure/confirmation request, following the existing PROPOSED-DEFAULT convention. No design change required unless the user confirms reading (b) was intended.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- DA-001-i4: Hedge or evidence the "generalizes cleanly to any other single operator" claim (re-label `[INFERENCE]` + narrow scope, or add one worked alternative-operator scenario). Wording/documentation fix only.

**P1 (Major — SHOULD resolve; require justification if not):**
- DA-002-i4: Add/replace the worked disambiguation example with the real `FU.1` collision already present in `FEEDBACK-LOG.md`, demonstrating the two-candidate enumeration.
- DA-003-i4: Reword "Index growth is bounded" to rate-bounded language; state the re-assessment trigger's fallback (even if deferred).
- DA-004-i4: Add a one-line confirmation request on the FU.5 "linked-list between logs" reading, following the existing PROPOSED-DEFAULT (Q1–Q4) pattern.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- DA-005-i4: Acknowledge the sealed-segment file-count growth as a disclosed, accepted operational trade (parallel to the existing discovery-cost disclosure).
- DA-006-i4: Acknowledge that the alias-field mechanism/protocol is installed framework-wide to accommodate one documented operator profile; note that non-restarting operators pay only the `(alias: —)` boilerplate cost, not the full disambiguation-protocol cost.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-003 (no defined index-overflow fallback), DA-004 (ambiguous requirement resolved silently), DA-005 (file-count growth undisclosed) |
| Internal Consistency | 0.20 | Negative | DA-001 (inference-labeling convention inconsistently applied to a universal generalization claim) |
| Methodological Rigor | 0.20 | Negative | DA-002 (disambiguation mechanism asserted but untested against a real, already-present collision) |
| Evidence Quality | 0.15 | Negative | DA-001 (unvalidated "any operator" claim), DA-003 ("bounded" wording outruns the math shown) |
| Actionability | 0.15 | Negative (minor) | DA-006 (framework-wide cost of a niche accommodation not fully acknowledged) |
| Traceability | 0.10 | Negative | DA-004 (ambiguous FU.5 requirement not traced to an explicit user confirmation) |

**Result:** 1 Critical, 3 Major, 2 Minor. Consistent with the task brief's framing, all six findings are wording/disclosure/confirmation fixes — none require new lint checks, new files, or new subsystems, preserving the anti-bloat posture already established across iterations 1–3. Overall assessment: **REVISE** (targeted). The Critical finding (DA-001) is the one item this executor recommends treating as a hard gate per the task brief's explicit "overclaimed coverage IS Critical" instruction; the three Major findings are all real, evidence-backed gaps (one of them — DA-002 — demonstrated with the package's own live data, not hypothesized) but do not individually invalidate the core design.
