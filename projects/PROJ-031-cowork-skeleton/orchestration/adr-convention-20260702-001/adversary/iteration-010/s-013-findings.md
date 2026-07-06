# Inversion Report: ADR-PROJ031-004 (v1.10 wire content, changelog shows through v1.11) + adr-standards-rule-draft.md

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-013, iteration 10, VERIFIED-CRITICALS protocol)
**H-16 Compliance:** S-003 embedded throughout the package's own options analysis (Options A-F steelmans); this iteration is blind to iteration-009/010 tournament siblings per protocol, but the package's extensive prior-iteration S-003 record is readable via `subtraction-pass-notes.md`.
**Goals Analyzed:** 3 (collision-free-enough ADR identity; honest promotion process; adoptable MEDIUM-tier convention) | **Assumptions Mapped:** 6 | **Vulnerable Assumptions Found:** 2 (1 Critical, 1 Major)

## Document Sections

| Section | Purpose |
|---|---|
| [Summary](#summary) | Overall verdict |
| [Goal Inventory and Inversion](#goal-inventory-and-inversion) | Stated goals, anti-goals, and null-alternative check |
| [Assumption Map](#assumption-map) | Explicit/implicit assumptions stress-tested |
| [Findings Table](#findings-table) | 013-00N summary |
| [Finding Details](#finding-details) | Full evidence and analysis |
| [Recommendations](#recommendations) | Mitigations |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |

---

## Summary

This iteration used Inversion (not Pre-Mortem/Devil's-Advocate re-litigation) to stress-test the package's load-bearing assumptions after 8 prior tournament rounds and a mature, extensively-disclosed residual register (R-1..R-17, R-A/B/C). The 17 prior Criticals are correctly dispositioned in `subtraction-pass-notes.md`, and the overwhelming majority of plausible attack surface is already named and honestly disclosed — those are **not** re-reported here per the mandate. Inverting the package's own core claim ("the grandfather regression test is green / the 18-file corpus passes L-1") surfaced **one genuine, previously-undisclosed internal contradiction** that would guarantee a concrete implementation failure of the collision-free-identity purpose if M-6 is built literally as specified in either document, plus **one genuine, previously-undisclosed implementation-mechanism gap** in the ratification-anchored grandfather baseline that risks silently recreating the exact amnesty-window bug the package's own 012-003 fix (iteration-9) believed it had closed. **Recommendation: REVISE** — both findings are text-only, doctrine-compatible fixes (no new lint rule, no new machinery), consistent with the subtraction doctrine already governing this package.

---

## Goal Inventory and Inversion

**Goal 1 (explicit):** ADR identity SHOULD be collision-free enough that the corpus never repeats the bare-`ADR-NNN`/`ADR-EPIC002-001` collision history (Context, ADR:73,113).
**Anti-goal:** guarantee failure by shipping a lint whose own "grandfather regression test" — the gate required before M-6 can ship (ADR:541, "with the grandfather regression test green") — is internally unsatisfiable or dishonestly reported as green. **013-001 shows the package currently does this**, at the specification level, for exactly the file class (`ADR-150-001`) the document itself repeatedly cites as the hard case.

**Goal 2 (explicit):** the promotion process SHOULD be honest, not merely asserted (Meta-Note, Promotion Process). **Anti-goal:** guarantee failure by making a "fixed" claim (012-003's ratification-anchored baseline) that lacks any actual reconstruction mechanism, so the fix is prose, not a procedure a future implementer can execute deterministically. **013-002 shows this gap is real and undisclosed.**

**Goal 3 (explicit):** the convention SHOULD be adoptable at MEDIUM tier. **Null-alternative check (IN-004, already in the deliverable):** the package's own null-alternative comparison is honest and largely defensible; inverting it did not surface a new failure beyond what R-B/012-001/FM-5 already disclose (guidance undiscoverable until M-2 lands, lint absent until M-6). Per the task mandate, that already-disclosed residual is **not** re-reported as a finding.

---

## Assumption Map (selected, Major+ only shown)

| # | Assumption | Type | Confidence | Consequence if wrong |
|---|---|---|---|---|
| A1 | L-1's "canonical OR dialect" grammar test, as literally defined in both documents, is what the grandfather regression test actually runs against the legacy corpus | Implicit (methodological) | Low — contradicted by the document's own text | Regression test cannot go green as specified; M-6 gate is unsatisfiable or falsely reported |
| A2 | "Ratification-anchored" grandfather baseline (012-003 fix) can be reconstructed by a future M-6 implementer without an explicit anchor mechanism | Implicit (operational) | Low — no anchor named anywhere in either file | The exact amnesty-window bug 012-003 claims to have fixed recurs silently at build time |
| A3 | The remaining assumptions (self-approvable MEDIUM override under solo maintainer; guidance undiscoverable pre-M-2; lint absent pre-M-6; entity-embedded/repository-topology out-of-scan; taxonomy synonymy unmitigated) | Explicit | High (all already disclosed as R-9..R-17, R-A/B/C) | **Already disclosed — not re-reported per mandate.** |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|---|---|---|---|---|---|---|
| 013-001 | L-1 grammar check ("canonical OR dialect") is what the grandfather regression test runs, and `ADR-150-001` is claimed to both fail it (by definition) and pass it (by regression-test requirement) | Assumption / Internal Contradiction | Low | **Critical** | ADR:226,229,328-329,541,686,691,693; rule-draft:70,94,175,181,183 | Internal Consistency, Methodological Rigor |
| 013-002 | The ratification-anchored grandfather baseline (012-003 fix) has a concrete, executable reconstruction mechanism | Assumption / Anti-Goal (undetected drift) | Low-Medium | **Major** | ADR:226-229 (counts only, no filename manifest),541,693; rule-draft:183 | Methodological Rigor, Actionability |

---

## Finding Details

### 013-001: L-1 grammar rule and the grandfather regression test directly contradict each other on `ADR-150-001` [CRITICAL]

**Type:** Assumption (methodological) / Internal Contradiction — verified by direct textual comparison, not inference.

**Original assumption (as the package presents it):** the 5-rule lint's L-1 rule ("Filename matches canonical OR dialect") is a complete, coherent PASS/FAIL test, and the mandatory "grandfather regression test" (M-6's ship gate) is simply that same test run once against the 18 pre-existing files to confirm none are wrongly rejected — the exact discipline iteration-1's P0-1 fix ("the FAIL-class lint no longer rejects the corpus it promises to grandfather," ADR Changelog:779) was supposed to guarantee holds forever.

**Inversion — what actually guarantees this fails:** the L-1 row's own definition, stated identically in **both** authoritative documents, names `ADR-150-001` as an example of a file that is **rejected** by the canonical-or-dialect test:
- ADR:686 — "the canonical slug begins with a letter, so `ADR-150-001` (numeric-leading) is rejected."
- rule-draft:175 — "rejects malformed IDs and numeric-leading slugs (`ADR-150-001`)."
- rule-draft:70 (ID Scheme) — "the leading slug token has to begin with a letter (so `ADR-150-001` is not a canonical slug; grandfathered)" — note this is the *only* place a caveat ("grandfathered") is attached, and even there it is a parenthetical gloss, not a stated third disjunct of the rule.
- ADR:328-329 (ID grammar comment) explicitly concedes `ADR-150-001` "matches neither grammar" and that "the grandfather allowlist relies on" that fact — confirming the document itself knows `ADR-150-001` cannot pass a literal canonical-or-dialect test.

Yet the same two documents require this exact file to **pass** L-1 as part of a hard ship-gate:
- ADR:226,229 — the D-4 reconciliation counts `150×1` inside the 16-file whole dialect corpus, and states "18 = the grandfather regression corpus that must pass L-1 = 15 dialect-reachable + 3 canonical" (150×1 is one of the 15 dialect-reachable — confirmed by the D-4 arithmetic, since only `ADR-STORY015-001` is named as the single out-of-scan exclusion).
- ADR:541 (Migration Plan M-6) — "Implement + wire the 5-rule L5 CI lint... with the grandfather regression test green (15 dialect reachable + 3 canonical = **18 files pass L-1**...)."
- ADR:691 / rule-draft:181 — "A grandfather regression test gates the lint before it ships: the 18 files reachable... pass L-1."
- ADR:693 / rule-draft:183 (the "IN-001-iter8" spec clarification) attempts to resolve this by declaring pre-existing files "grandfathered-exempt from L-1/L-2, not... newly-minted" — but this exemption is stated only as free-standing prose **after** the L-1 rule's own row definition, and is never folded back into L-1's own stated test ("canonical OR dialect"). L-1's row-level definition in both documents is not amended to read "canonical OR dialect OR present on the ratification-time baseline" — it still flatly asserts `ADR-150-001` "is rejected."

**Why this is not merely wording, and not an already-disclosed residual:** the deleted **L-12 "grandfather-allowlist freeze"** rule (subtraction-pass-notes.md:59, "12 deleted outright... L-12") was precisely the mechanism that would have let a matches-neither-grammar legacy file like `ADR-150-001` pass as an explicit allowlist entry. When L-12 was deleted in the subtraction pass (v1.7) to reach the 5-rule core, its function was informally reattached to L-1 via the iteration-8 "IN-001" prose clarification (ADR:693) — but that reattachment was never written into L-1's own operative definition in either document's lint-specification table. The result: an implementer who builds L-1 literally as specified ("Filename matches canonical OR dialect") and then runs the mandatory grandfather regression test will find `ADR-150-001` **fails** — reproducing, for a real named file, the exact "lint rejects the corpus it promises to grandfather" defect class that iteration-1's P0-1 fix (ADR Changelog v1.1) was created to eliminate. This is not listed among R-1..R-17/R-A/B/C, and it directly threatens the standard's stated purpose (collision-free-enough identity delivered via a lint that must first prove it does not break on the very corpus it grandfathers).

**Plausibility:** High — this is not a hypothetical inversion, it is a demonstrable textual contradiction between two co-authoritative passages, present today in both files.

**Consequence:** If M-6 is implemented literally from either document's L-1 row, the mandatory pre-ship regression test cannot go green without an undocumented ad-hoc fix invented at build time — or it is marked green by silently special-casing a file the rule's own text says is rejected, which is exactly the kind of quiet overclaim the package's subtraction doctrine and P-022 discipline otherwise polices rigorously everywhere else in this document.

**Dimension:** Internal Consistency (primary); Methodological Rigor (the regression-test gate is not actually well-defined).

**Mitigation:** Fold the grandfather-baseline exemption into L-1's own row definition in both documents, e.g.: "Filename matches canonical OR dialect OR is present on the ratification-time grandfather baseline list (see [baseline mechanism])." Text-only fix; no new rule, no reintroduction of L-12 as a separate rule ID — consistent with the existing "spec wording, not a sixth rule" framing already used for the IN-001-iter8 clarification.

**Acceptance Criteria:** L-1's row definition, in both the ADR Enforcement Design table and the rule-draft L5 CI Lint Specification table, explicitly states the three-way disjunction (canonical / dialect / ratification-baseline-listed), and no sentence anywhere asserts `ADR-150-001` "is rejected" without that qualifier attached in the same sentence.

---

### 013-002: The "ratification-anchored" grandfather baseline (012-003 fix) has no executable reconstruction mechanism [MAJOR]

**Type:** Assumption (operational) — an undetected gap in an already-fixed finding's implementation path.

**Original assumption:** iteration-9's 012-003 fix re-anchored the grandfather baseline from "when the lint ships" to "ratification time (2026-07-05/06)" specifically to prevent a growing post-ratification amnesty window (ADR:693, rule-draft:183: "captured **once** as a data list in M-6, a one-time artifact, not standing machinery... Anchoring to ratification, not lint-ship, is deliberate"). The implicit assumption is that this re-anchoring is itself something a future M-6 implementer can actually **execute**.

**Inversion — what would guarantee this fails:** M-6 has "no committed ship date" (ADR:501, FM-5, rated the single best-evidenced risk: "M-2, M-6 and M-12 all stay untracked TBD-Tasks"). Neither document names a git commit SHA, tag, or any other durable anchor for "ratification time" — grep across both files for `git tag`, `commit sha`, `--before`, `git log`, `git ls-tree`, or any equivalent reconstruction primitive returns nothing (verified 2026-07-06). Nor does either document contain an actual **enumerated filename list** of the 18/15/16-file corpus — only aggregate per-family counts (ADR:226, "`EPIC002`×2, `PROJ010`×6, `PROJ022`×2, `PROJ031`×4, `STORY015`×1, `150`×1 = 16"). A future implementer building M-6 — possibly months after ratification, per FM-5's own risk framing — has no deterministic way to reconstruct "the corpus as it stood on 2026-07-05/06" from either document; the only practical options are (a) manually diffing `git log` around that date without a named anchor (error-prone, not specified as a step), or (b) simply running `find` at build time and treating whatever exists then as "the baseline" — which is precisely the undated, lint-ship-time anchoring behavior 012-003 says it rejected. This is a real, disclosed-adjacent-but-currently-undisclosed operational gap: the *policy* was fixed (anchor to ratification time), but the *procedure* to actually do so was not specified, so the fix is not yet load-bearing.

**Plausibility:** Medium-high — given FM-5's own admission that M-2/M-6/M-12 may never be tracked or may land arbitrarily late, the ratification-to-build gap this finding depends on is exactly the gap the package's own Pre-Mortem already rates as the most likely failure mode.

**Consequence:** Without an anchor, the 012-003 fix is aspirational text rather than an instruction a future maintainer can follow correctly; the amnesty-window bug it targeted can recur silently, and no lint rule or disclosed residual currently names this gap.

**Dimension:** Methodological Rigor (a stated fix lacking an executable procedure); Actionability (the M-6 migration row does not include the step this finding would add).

**Mitigation:** Either (a) tag the ratification commit now (e.g., `git tag adr-convention-ratified-20260705`) and reference that tag as the baseline anchor in both documents, or (b) embed a literal enumerated filename manifest (not just family counts) as an appendix/data block in the rule draft, to be copied verbatim into M-6's implementation rather than reconstructed from git history. Either is a text/tooling-light fix compatible with the subtraction doctrine (no new lint rule; a one-time data-capture or tag, matching the "one-time artifact, not standing machinery" framing already used at ADR:693).

**Acceptance Criteria:** The Migration Plan (M-6 row) or the L5 CI Lint Specification names a concrete, non-git-dependent-on-memory mechanism (a tag reference or an embedded filename list) for reconstructing the ratification-time baseline, so the 012-003 fix is executable by whoever eventually builds M-6, not only stateable by whoever wrote this ADR.

---

## Recommendations

| Priority | ID | Action | Acceptance Criteria |
|---|---|---|---|
| MUST (before this package can honestly claim its grandfather regression test is green) | 013-001 | Fold the baseline exemption into L-1's own operative definition in both files | No sentence asserts `ADR-150-001` "is rejected" without the baseline-exemption qualifier in the same breath; L-1 row states the 3-way disjunction |
| SHOULD | 013-002 | Name a concrete ratification-baseline reconstruction mechanism (git tag or embedded filename manifest) | M-6 row or L5 spec names the mechanism; no reliance on an implementer's undocumented judgment call at build time |

Both fixes are text-only and additive-doctrine-compliant (no new lint rule, no ledger, no gate) — consistent with the subtraction pass's own remediation style for every prior iteration.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|---|---|---|---|
| Completeness | 0.20 | Neutral | Both findings are narrow, targeted gaps in an otherwise exceptionally complete disclosure regime; they do not indicate missing analysis elsewhere |
| Internal Consistency | 0.20 | **Negative** | 013-001 is a direct, evidenced self-contradiction between the L-1 rule's own definition and the mandatory regression-test claim, present in both authoritative documents |
| Methodological Rigor | 0.20 | **Negative** | 013-001 (the ship-gate is not actually well-defined for a named edge case) and 013-002 (a stated fix lacking an executable procedure) both weaken the rigor of the enforcement design specifically |
| Evidence Quality | 0.15 | Neutral | Both findings are grounded in direct quotation and grep-verified absence, not speculation |
| Actionability | 0.15 | Negative (013-002 only) | 013-002 identifies a fix-the-policy-not-the-procedure gap; the recommended mitigation is concrete and low-cost |
| Traceability | 0.10 | Neutral | Findings cite exact file+line for every claim |

---

## Execution Statistics

- **Total Findings:** 2
- **Critical:** 1
- **Major:** 1
- **Minor:** 0
- **Protocol Steps Completed:** 6 of 6 (goals stated, anti-goals inverted, assumptions mapped, stress-tested, mitigations developed, scoring impact synthesized)
- **Already-disclosed residuals reviewed and excluded per mandate:** R-1..R-17, R-A, R-B, R-C, and all 17 prior-iteration Criticals in `subtraction-pass-notes.md`
