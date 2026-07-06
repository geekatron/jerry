# Red Team Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft — Iteration 6 (Post-Subtraction)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-05
**Reviewer:** adv-executor (blind, independent reviewer — no access to sibling iteration-6 adversary outputs)
**H-16 Compliance:** Not independently verifiable by this agent (no S-003 artifact was provided in this invocation's context); per the deliverable's own glossary note (`ADR-PROJ031-004:67`), S-003 influence is embedded, not separately filed for this iteration. Proceeding per task mandate — flagged, not blocking, since S-001 is required-not-optional at C4 regardless and the orchestrator controls strategy sequencing (P-020: outside this agent's mandate to halt the tournament).
**Threat Actor:** A time-pressured or careless contributor (or an adversarial prober) operating in a distributed, uncoordinated, multi-branch repo with no central ID registry (c-006) and no CODEOWNERS gate. Goal: mint a new ADR quickly without doing taxonomy/collision homework, or deliberately test whether the convention's claimed collision-safety guarantees actually hold. Capability: full write access to any `projects/*/decisions/` or `docs/design/` path; public knowledge of the ID grammar and the exact lint specification (both are published in the reviewed files); awareness that enforcement is currently advisory-only (lint not built) and, once built, is override-with-justification with no waiver ledger. Motivation: ship without friction, or expose a gap between what the lint *claims* to catch and what it *actually* catches.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All RT-findings at a glance |
| [Finding Details](#finding-details) | Full attack-vector writeups with evidence |
| [Recommendations](#recommendations) | P0/P1/P2 countermeasure plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Finding counts |

---

## Summary

The slimmed (post-subtraction) design is a sound MEDIUM-tier posture in principle — grandfathering, a permitted dialect, no big-bang renumber, and an honestly-labeled designed-not-built lint. However, red-teaming the **specific literal mechanism** given for collision detection (L-1 grammar, L-3 duplicate-ID dedup) finds that a contributor **can** mint colliding and shadowing IDs the 5-rule core misses, and — critically — two of these gaps are **CLAIMED as covered** in the deliverable's own prose rather than disclosed as residuals (which is the disqualifying condition per this review's mandate). The single most damaging finding (RT-101) is that the literal `L-3` dedup mechanism, presented twice ("exactly what lint L-3 runs in CI") in both documents, silently excludes the **entire dialect-ID family** — the exact class of the historical `ADR-EPIC002-001` collision this ADR uses as its central motivating evidence — from duplicate detection, due to a case-sensitivity bug in the extraction regex. A second finding (RT-102) shows the explicit claim that L-1 "rejects... case-folded entity-prefix look-alikes" is not implemented by the grammar regex actually given. **Recommendation: REVISE.** The overall architecture does not need to be rejected or re-expanded with new machinery (that would repeat the additive-remediation spiral this pass was meant to end) — it needs two narrowly-scoped regex/prose corrections plus one honest re-disclosure, all consistent with the subtraction pass's own "close by deleting the false claim, don't add machinery" doctrine.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|-----------------|----------|----------|---------|---------------------|
| RT-101-iter6 | L-3 dedup regex silently excludes ALL dialect-family IDs (case-sensitivity bug); the historical `ADR-EPIC002-001` collision would recur undetected | Rule circumvention | High | Critical | P0 | Missing (claimed as covered) | Methodological Rigor, Internal Consistency |
| RT-102-iter6 | L-1 grammar's claimed rejection of "case-folded entity-prefix look-alikes" (`ADR-proj031-001`) is not implemented by the given canonical regex | Ambiguity exploitation | High | Critical | P0 | Missing (claimed as covered) | Evidence Quality, Internal Consistency |
| RT-103-iter6 | L-7 "relationship target resolves" checks existence only, not bidirectional/semantic correctness — a mismatched or shadow target can pass | Boundary violations | Medium | Major | P1 | Partial | Completeness |
| RT-104-iter6 | R-6 residual (cross-branch same-slug race) states detection "via L-3 `sort\|uniq -d`" without disclosing that, per RT-101, this detection is 0% for dialect-form races, not merely "mitigated" | Degradation paths | Medium | Major | P1 | Partial (overstated) | Traceability, Internal Consistency |
| RT-105-iter6 | The 19-file grandfather regression test validates only L-1 grammar-matching; it does not regression-test L-3 dedup correctness or the specific case-fold adversarial case, despite the deliverable's own prior institutional history with a "lowercase-only defect" | Degradation paths | Low | Minor | P2 | Missing | Methodological Rigor |

---

## Finding Details

### RT-101-iter6: L-3 duplicate-ID lint silently excludes the entire dialect-ID family [CRITICAL]

**Attack Vector:** The companion rule draft's L5 CI Lint Specification states L-3 as: *"Extract `{slug}-NNN` of all non-frozen ADRs; `sort | uniq -d` must be empty. **Repo-wide.**"* (`projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:173`). Both documents then give the **identical concrete implementation**, explicitly labeled as *"exactly what lint L-3 runs in CI"* (rule draft `:179`; ADR `:391`, restated at ADR `:653`):

```
find projects docs/design -path '*/decisions/*' -name 'ADR-*.md' \
  -not -path '*/docs/adrs/*' -not -path '*/docs/archive/*' \
  | sed -E 's#.*/(ADR-.*)\.md#\1#' \
  | grep -E '^ADR-[a-z0-9-]+-[0-9]{3}' \
  | sed -E 's/^(ADR-[a-z0-9-]+-[0-9]{3}).*/\1/' \
  | sort | uniq -d
```
(rule draft `:181-189`; ADR `:393-401`, identical pattern)

The extraction step `grep -E '^ADR-[a-z0-9-]+-[0-9]{3}'` uses a **lowercase-only** character class (`[a-z0-9-]`) with no `-i` flag. A dialect filename such as `ADR-PROJ031-005-foo.md` (or `ADR-EPIC002-001-*.md`, the historically-collided ID cited at `ADR-PROJ031-004:113`) reduces to `ADR-PROJ031-005-foo`; immediately after the literal `ADR-` the next character is uppercase `P`, which does not belong to `[a-z0-9-]`. Because the pattern is start-anchored (`^`), the whole line fails to match and is **dropped by the grep filter** — it never reaches the `sort | uniq -d` step at all. This is a **structural, complete (not probabilistic) exclusion**: by construction, every filename that passes `L-1`'s dialect grammar (the closed `{PROJ|EPIC|FEAT|STORY}\d{3}` prefix set, which is uppercase per `ADR-M-003`/rule draft `:71`) is precisely the class this extraction regex cannot match, since `L-1`'s canonical grammar requires the domain-slug to start with a lowercase letter (rule draft `:70`) and its dialect grammar requires the uppercase closed set — there is no filename that is simultaneously grammar-valid and lowercase-dialect. **Every legitimate dialect ADR is therefore invisible to L-3's literal dedup mechanism.**

**Exploitability:** High — no special access or timing is required beyond ordinary distributed authorship. Two contributors on different branches (or the same contributor twice) can independently author `ADR-PROJ031-006-alpha.md` and `ADR-PROJ031-006-beta.md` (different title-slug tails, so no git path/merge conflict) inside the *same* project's `decisions/` directory. Both pass L-1 (grammar OK), both pass L-4 (both correctly located under `PROJ031`), and — per this finding — **both are silently dropped from L-3's extraction**, so `sort | uniq -d` reports nothing. The duplicate `ADR-PROJ031-006` identity ships undetected by any of the 5 rules.

**Severity:** Critical — this is not a hypothetical edge case; it defeats the deliverable's own headline historical justification. The ADR repeatedly cites the real `ADR-EPIC002-001` collision (`ADR-PROJ031-004:113`, `:150`, `:430`) as the empirical evidence motivating the entire lint requirement, and states the corpus is "grandfathered in place... collision-*resistant*... no live intra-family duplicate remains **after** the rename" (`ADR-PROJ031-004:485`, Migration Plan row 2) — implying the L5 lint is the forward-looking guarantee against recurrence. It is not: the exact collision class that already happened once is structurally invisible to the literal L-3 mechanism as specified.

**Existing Defense:** Missing, and — this is the aggravating factor — **claimed as present**, not disclosed as absent. Compare to the deliverable's own disclosure discipline elsewhere (R-6, R-7, R-B, R-C are all explicitly labeled `[INHERENT]`/residual with a Claim-Status tag); no equivalent disclosure exists for "L-3 does not dedup dialect-form IDs." The rule draft's own wording ("all non-frozen ADRs... Repo-wide") is an unqualified coverage claim.

**Evidence (internal inconsistency, corroborating the defect is real and not a deliberate scope choice):** The ADR's own "Testing / verification approach" section narrows the claim without flagging it as a narrowing: *"(2) `sort | uniq -d` over extracted **canonical** IDs is empty"* (`ADR-PROJ031-004:389`, emphasis added) — "canonical," not "all non-frozen." This contradicts the rule draft's "all non-frozen ADRs... Repo-wide" (`:173`) and the ADR's own Enforcement Design mirror of the same row (`:650`). Two sections of the same document family describe different scopes for the identical rule, which is itself evidence the authors did not realize the extraction regex silently narrows the claim.

**Dimension:** Methodological Rigor (the stated mechanism doesn't do what it says); Internal Consistency (the two scope-descriptions of L-3 contradict each other).

**Countermeasure:** Either (a) fix the extraction regex to be case-insensitive or to explicitly union both grammars, e.g. `grep -Ei '^ADR-[a-z0-9-]+-[0-9]{3}'` (case-insensitive) or two patterns covering canonical (`[a-z]...`) and dialect (`(PROJ|EPIC|FEAT|STORY)\d{3}`) unioned before `sort | uniq -d`; or (b), consistent with the subtraction pass's own doctrine of honest disclosure over added machinery, **narrow the claim to match reality** ("L-3 dedups canonical (lowercase-slug) IDs repo-wide; dialect-family `NNN` reuse within a project is NOT checked and is a disclosed residual") and add it to the Residuals table alongside R-6/R-7. Either resolution is acceptable under this ADR's own MEDIUM-tier philosophy; what is not acceptable is the current state, where the text claims coverage the mechanism does not provide.

**Acceptance Criteria:** Construct a two-file test fixture (`ADR-EPIC002-099-a.md`, `ADR-EPIC002-099-b.md`) and re-run the published pre-flight one-liner (both copies, rule draft and ADR); it must either report the duplicate (if (a) is chosen) or the documents must state plainly, next to both copies of the one-liner and the L-3 table row, that dialect-form duplicates are not caught by it (if (b) is chosen).

---

### RT-102-iter6: L-1's claimed rejection of case-folded dialect look-alikes is not implemented [CRITICAL]

**Attack Vector:** Both documents explicitly claim L-1 blocks case-folded entity-prefix look-alikes:
- Rule draft: *"**L-1 Grammar** | Filename matches canonical OR dialect ([ID Scheme](#id-scheme)) — rejects malformed IDs and **entity-prefix look-alikes masquerading as domain slugs**."* (`:171`)
- ADR: *"**L-1 Grammar** | Filename matches canonical OR dialect... the canonical slug MUST begin with a letter, so `ADR-150-001` and **case-folded entity-prefix look-alikes (`ADR-proj031-001`) are rejected**."* (`:648`)

But the actual canonical regex given in **both** documents' own grammar sections is: `^ADR-[a-z][a-z0-9]*(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$` (rule draft `:70`; ADR `:313`), whose only stated exclusion is a **numeric-leading** first character (so `ADR-150-001` is excluded — that part of the claim is true). Nothing in this pattern excludes a domain-slug token that happens to be the lowercase form of a dialect prefix. `proj031` fully satisfies `[a-z][a-z0-9]*` (letter `p`, then digits `roj031`... more precisely `p` then `roj031` all lowercase-alnum) — there is **no character-class or lookahead rejecting known dialect words in lowercase**. A file named `ADR-proj031-001-shadow.md` therefore **passes** the canonical grammar as literally specified, directly contradicting the "are rejected" claim.

**Exploitability:** High — trivial to construct; requires only choosing a domain-slug that happens to case-fold-match `proj\d{3}`, `epic\d{3}`, `feat\d{3}`, or `story\d{3}`. No coordination or timing needed.

**Severity:** Critical — this produces a filename that is simultaneously (a) grammar-valid, (b) visually near-identical to the real dialect ID it shadows (differing only in case), and (c) — per RT-101 — tracked as an *entirely separate* identity in L-3's extraction (since it's lowercase, it *is* picked up by the buggy regex, unlike the genuine dialect ADR it shadows). A contributor or automated tool relying on case-sensitive `grep -r "ADR-EPIC002"` to audit the EPIC002 family would silently miss `ADR-epic002-001-shadow.md` entirely (wrong case), while a human skimming a directory listing could easily mistake the two for the same decision. This directly undermines the "grep-friendly, self-describing, always-current" discoverability property the ADR repeatedly claims as B's core advantage (`ADR-PROJ031-004:265`, `:409`).

**Existing Defense:** Missing, and explicitly claimed as present in **both** companion documents (`rule-draft:171`, `ADR:648`) — the double occurrence rules out a one-off typo and indicates this claim is treated as an established fact of the design.

**Evidence of regression (not a fresh oversight, a dropped mechanism):** Changelog v1.2 records: *"(P0-7/RT-003) banned case-folded dialect look-alike slugs in **L-1a**"* (`ADR-PROJ031-004:738`) — i.e., a pre-subtraction iteration of this design **did** have a dedicated sub-rule for exactly this case. The subtraction pass collapsed the split "L-1a canonical / L-1b uppercase-dialect" structure (introduced in v1.1, `:737`: *"split the L-1 lint into disjunctive L-1a canonical / L-1b uppercase-dialect"*) back into a single "L-1 Grammar: matches canonical OR dialect" rule, but the **claim text describing what L-1 rejects was not updated to reflect the loss of the dedicated case-fold check**. This is a direct, evidenced instance of the additive-then-subtractive history leaving a stale, over-claiming sentence behind — precisely the failure mode this iteration was asked to hunt for.

**Dimension:** Evidence Quality (the claim is not backed by the regex actually given); Internal Consistency (rule draft `:68` itself warns "a lowercase-only regex would wrongly reject grandfathered uppercase dialect ADRs" — i.e. the authors were alert to one direction of the case-sensitivity problem but not the other).

**Countermeasure:** Add an explicit negative-lookahead (or a post-regex programmatic check in the eventual `scripts/lint_adr_convention.py`) rejecting any canonical-looking domain-slug whose case-folded form exactly matches `(proj|epic|feat|story)\d{3}` as its leading token — restoring the protection the pre-subtraction `L-1a/L-1b` split provided, without reintroducing the split's full complexity. This is a single, cheap, deterministic regex addition, not new machinery in the sense the subtraction pass was correcting for.

**Acceptance Criteria:** Attempt to author `ADR-proj031-001-shadow.md` and `ADR-epic002-099-test.md`; the lint (once built, M-6) must reject both, and the claim text should cite the actual mechanism that does so (not an aspirational restatement of a deleted L-1a rule).

---

### RT-103-iter6: L-7 verifies relationship-target *existence*, not correctness [MAJOR]

**Attack Vector:** L-7 is specified as: *"`superseded_by`/`promoted_to`/`promoted_from` targets resolve to an existing ADR — catches a half-completed Path-2 orphaning the source."* (rule draft `:175`; ADR `:652`). This checks only that the referenced ID string **resolves to some existing file** — it does not check that the relationship is reciprocal (target's own `supersedes`/`promoted_from` points back) or that the target is the *semantically correct* ADR. A contributor (or a careless Path-2 promotion, per `ADR-PROJ031-004:511` M-9) could set `promoted_to: ADR-agent-design-001` (a real, unrelated, existing ADR) by typo or copy-paste error; L-7 as specified would report this as **PASS** ("resolves to an existing ADR"), even though the relationship is semantically wrong. Combined with RT-102, a shadow ID (`ADR-proj031-001-shadow.md`) is itself a real, existing file once created, so `promoted_to`/`superseded_by` pointed at it would also resolve — L-7 cannot distinguish a shadow target from a legitimate one.

**Exploitability:** Medium — requires either a typo/copy-paste error (plausible, unforced) or deliberate misuse combined with RT-102 (requires intent).

**Severity:** Major — misdirects provenance/supersession chains without any lint signal; a reader following `promoted_to` lands on the wrong decision. Does not invalidate the whole scheme (most relationship edits will be correct in practice), but is a real, uncaught defect class within the scheme's own consistency guarantees.

**Existing Defense:** Partial — existence-checking catches the *orphaning* failure mode it was designed for (a Path-2 promotion that forgets to point back, per the historical `ADR-PROJ007-001/002` wound this ADR cites); it does not catch a *misdirected-but-resolvable* target. Note the deliverable's own Changelog v1.2 (`:738`) states L-7 was "made bidirectional + FAIL-class" in a prior iteration ("P1-4/RT-005"), which if still true would substantially close this gap (bidirectional checking catches most misdirection, since a wrong target's own back-link would not point to the source) — but the **current** L-7 row text in both documents (rule draft `:175`, ADR `:652`) does not restate "bidirectional" and reads as existence-only. This ADR agent cannot verify from the current text alone whether bidirectionality survived the subtraction pass or was silently dropped along with the other 13 rules — flagged as an open ambiguity, not asserted either way (P-022).

**Dimension:** Completeness (relationship-integrity coverage is narrower than the historical "bidirectional" claim implies).

**Countermeasure:** Explicitly restate in both documents whether L-7 checks bidirectionality (if yes: state it in the rule row text, not just the changelog; if no, post-subtraction: disclose the narrowing the same way other subtraction-pass narrowings are disclosed).

**Acceptance Criteria:** The L-7 row text in both documents states, unambiguously, whether reciprocal-link checking is in scope.

---

### RT-104-iter6: R-6's stated detection mechanism is inaccurate for the dialect sub-case [MAJOR]

**Attack Vector:** The Risks table states: *"R-6: Cross-branch same-slug `NNN` race... Detection is post-hoc at merge via **L-3 `sort|uniq -d`** (CI) and the pre-flight collision command (local, run before commit). Accepted as a bounded residual... reduced and detected, not structurally prevented."* (`ADR-PROJ031-004:451`). This framing implies detection exists (reduced, not eliminated) for cross-branch races generally. Per RT-101, for **dialect-form** IDs specifically, L-3 provides **zero** detection (not "reduced" — absent), since the extraction regex never sees them. R-6's disclosure is honest and well-labeled for the *canonical*-slug race it was written for, but it does not carve out that the *dialect* sub-case (which is exactly the historically-collided `ADR-EPIC002-001` case) has no L-3 backstop at all.

**Exploitability:** Medium — same mechanism as RT-101; this finding is about the accuracy of the risk disclosure, not a new technical vector.

**Severity:** Major — a reader relying on R-6's disclosure to gauge residual risk for dialect ADRs would under-estimate it, since the text reads as uniformly "mitigated-not-eliminated" rather than "not mitigated at all for this sub-case."

**Existing Defense:** Partial (the disclosure exists and is honestly framed for canonical IDs; it is simply incomplete for dialect IDs).

**Dimension:** Traceability (residual disclosure does not trace to the actual, sub-case-specific coverage); Internal Consistency (same root cause as RT-101).

**Countermeasure:** Split R-6 into an explicit two-part disclosure: canonical-slug race (detected post-hoc by L-3) vs. dialect-family race (not detected by any of the 5 rules; mitigated only by the smaller blast radius of a single project's authors noticing a duplicate NNN by inspection).

**Acceptance Criteria:** R-6's row (or a new R-6b) states the dialect-family detection gap explicitly, once RT-101 is resolved one way or the other.

---

### RT-105-iter6: Grandfather regression test does not cover the exploited defect classes [MINOR]

**Attack Vector:** The mandated regression test validates that "all 16 live dialect files... and the 3 canonical `docs/design/` ADRs pass **L-1**" (`ADR-PROJ031-004:653`; rule draft `:653`-equivalent at `:94`). This is described as "the dry-run-against-the-real-corpus step whose absence caused **an earlier lowercase-only defect**" — i.e., the authors have direct institutional memory of exactly this class of regex bug (case-sensitivity around canonical vs. dialect forms), yet the regression test as scoped checks only that existing files pass grammar matching (L-1); it does not include a fixture that would have caught RT-101 (a synthetic duplicate dialect-ID pair run through the L-3 extraction) or RT-102 (a synthetic case-folded look-alike run through L-1). The lesson from the earlier defect was applied narrowly (to the corpus-pass regression) rather than generalized into an adversarial-fixture regression covering the same defect *class*.

**Exploitability:** Low (this is a testing-process gap, not itself directly exploitable).

**Severity:** Minor — a process improvement, not a live vulnerability.

**Existing Defense:** Missing.

**Dimension:** Methodological Rigor.

**Countermeasure:** When M-6 ships, add the two adversarial fixtures named in RT-101/RT-102's acceptance criteria to the regression suite, not just the 19-file grandfather corpus pass.

**Acceptance Criteria:** M-6's regression suite includes at least one red-then-green fixture for dialect-ID duplication and one for case-fold look-alike rejection.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance of the enforcement design; does not require reopening the ratified Decision itself, D-1 through D-5):**
- RT-101 — Fix the L-3 extraction regex (case-insensitive or dual-pattern) **or** honestly narrow the "all non-frozen ADRs... Repo-wide" claim to "canonical (lowercase-slug) IDs only" in both documents and add the dialect-dedup gap to the Residuals table.
- RT-102 — Add the case-fold-look-alike rejection back into L-1 (a single regex/lookahead addition), or delete the "case-folded entity-prefix look-alikes... are rejected" claim from both documents if the check is not restored.

**P1 (Important — SHOULD resolve, targeted edits, no new machinery):**
- RT-103 — State plainly whether L-7 checks bidirectionality; if not, disclose the semantic-mismatch gap.
- RT-104 — Split R-6 to disclose the dialect-sub-case detection gap explicitly (dependent on RT-101's resolution).

**P2 (Monitor):**
- RT-105 — Extend the future M-6 regression suite with the two adversarial fixtures above.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-103: relationship-integrity checking narrower than implied |
| Internal Consistency | 0.20 | Negative | RT-101/RT-102/RT-104: rule draft vs. ADR give different scopes for the same L-3 rule; L-1's claimed exclusion is not implemented; R-6 doesn't carve out the dialect sub-case |
| Methodological Rigor | 0.20 | Negative | RT-101/RT-105: the concrete mechanism given for "exactly what L-3 runs in CI" does not do what the surrounding prose claims, and the regression test does not cover the defect class the authors have institutional history with |
| Evidence Quality | 0.15 | Negative | RT-102: a twice-stated claim ("rejects... look-alikes") is not supported by the regex actually given in either document |
| Actionability | 0.15 | Positive | All five countermeasures are concrete, cheap (regex or one-sentence disclosure edits), and consistent with the subtraction pass's own doctrine — no new machinery required |
| Traceability | 0.10 | Negative | RT-104: R-6's residual disclosure does not trace accurately to the dialect-form detection gap |

**Overall assessment:** Targeted remediation required (REVISE), not a wholesale rejection of the post-subtraction design. The MEDIUM-tier posture, permitted dialect, and grandfathering remain sound; the defect is narrowly confined to two regex/claim mismatches (RT-101, RT-102) plus two disclosure-accuracy follow-ons (RT-103, RT-104), all fixable without reintroducing the additive-remediation spiral the subtraction pass was meant to end.

---

## Execution Statistics

- **Total Findings:** 5
- **Critical:** 2
- **Major:** 2
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5 (Threat Actor Defined; Attack Vectors Enumerated ≥4; Defense Gaps Assessed; Countermeasures Developed; Synthesis/Scoring Impact produced)
