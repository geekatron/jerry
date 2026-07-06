# Inversion Report: ADR-PROJ031-004 + Companion Rule Draft (Iteration 8, Post-Subtraction Package)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 | **Engagement gate:** 0.95
**Date:** 2026-07-06
**Reviewer:** adv-executor (blind, independent — S-013 lane only)
**H-16 Compliance:** S-003 Steelman applied within the deliverable itself (embedded per H-16, see ADR reading-note glossary); prior iterations' S-003/S-002/S-004/S-012 outputs not read (blind protocol) — this report treats the package as-is per the invoking instructions.
**Goals Analyzed:** 5 | **Assumptions Mapped:** 4 (stress-tested) | **Vulnerable Assumptions:** 4 (1 Critical, 3 Major) + 1 Minor traceability note

## Document Sections

| Section | Purpose |
|---|---|
| [Summary](#summary) | Overall verdict |
| [Step 1-2: Goals and Anti-Goals](#step-1-2-goals-and-anti-goals) | What would guarantee failure |
| [Step 3-4: Assumption Map and Stress Tests](#step-3-4-assumption-map-and-stress-tests) | Findings table |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Dimension mapping |
| [Null-Alternative Reassessment](#null-alternative-reassessment) | Direct answer to the benchmark question |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Summary

The post-subtraction package is honest, extraordinarily self-disclosed, and the underlying Scheme B decision is sound. Independent verification (Glob + targeted Read against the live repo, not against the package's own claims) confirms the package's self-reported facts are almost all accurate — the 18-file grandfather count reconciles, the citation ratios are plausible, and the producer-agent defects are exactly as described. However, inversion analysis surfaces one **previously-undisclosed Critical defect**: the subtraction pass deleted lint rule **L-12 (grandfather-allowlist freeze)** as part of removing the waiver-ledger machinery, but L-12 was also the *only* mechanism that would have operationalized "pre-adoption grandfathered" as anything more than an adjective — without it, the retained 5-rule core has no way to distinguish a legitimately-grandfathered legacy file from a "new bare ADR" the moment that file is next touched, and at least one live file (`ADR-150-001`) will fail this test on its next edit. Two further Major findings sharpen already-disclosed risks from "modeled future scenario" to "independently verified present fact" (the guidance is not loaded anywhere an agent would see it, and the manual citation-sweep mitigation has no trigger). **Recommendation: REVISE** — not because the design direction is wrong, but because IN-001 is a concrete, fixable design gap the subtraction doctrine itself would want closed (a data/scope fix, not new machinery), and IN-002/IN-003 should be reframed from hedged risk to confirmed current state before the package is scored again.

---

## Step 1-2: Goals and Anti-Goals

**Goals (restated, measurable):**
- G1: ADR promotion (project -> framework) becomes citation-stable (`git mv`, no rename) for the majority case.
- G2: Eliminate the bare-`ADR-NNN` collision failure mode and the opaque-origin discoverability failure mode.
- G3 (implicit but load-bearing): The convention actually becomes an operative norm — loaded, followed, and enforced by *something* — not merely a design artifact.
- G4: Remain MEDIUM-tier, honestly-scoped, and genuinely slim post-subtraction (no re-grown machinery).
- G5: Preserve citation integrity across the full ADR lifecycle (promotion, supersession, amendment), the founding motivating wound.

**Anti-goals ("what would guarantee failure?") and whether the package currently exhibits them:**

| Anti-goal | Guarantees failure of | Present in package today? |
|---|---|---|
| AG1: Bury the guidance where no consumer ever loads it; open zero tracked follow-through | G3 | **YES — verified, see IN-002** |
| AG2: Leave the ADR-producing agent emitting non-compliant IDs indefinitely | G1, G3, G5 | **YES — verified, see IN-002** |
| AG3: Let the only historically-observed promotion path (Path-2/rename) recur with an unenforced, untriggered manual citation cleanup | G1, G5 | **YES — see IN-003** (already partly disclosed as R-B, sharpened here) |
| AG4: Ship a "designed" lint whose own stated grammar rejects a file it promises to grandfather | G4, G5 | **YES — newly identified, see IN-001** |
| AG5: Claim the winner beats the null alternative using end-state evidence while the current state has not yet realized any of that evidence | Honest verdict framing | **Partially — see IN-004** |

---

## Step 3-4: Assumption Map and Stress Tests

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260706 | The retained 5-rule lint core (L-1 grammar + "pre-adoption grandfathered") correctly implements grandfathering without the deleted L-12 allowlist mechanism | Assumption | Low | **Critical** | `adr-standards-rule-draft.md:70-71,94`; ADR `:223,667,672`; `subtraction-pass-notes.md:57` | Methodological Rigor / Completeness |
| IN-002-20260706 | The FM-5 "nothing lands" scenario is a *future* risk, not the *current* state | Anti-Goal | High (confirmed) | Major | `.context/rules/adr-standards.md` (Glob: absent); `CLAUDE.md:51-63` (no entry); `projects/PROJ-031-cowork-skeleton/work/**` (Glob: no ADR-convention Task); `skills/problem-solving/agents/ps-architect.md:218,260,263,267-268` | Traceability |
| IN-003-20260706 | The R-B manual `grep`/`gh issue list` sweep ("owner: governance; cadence: at each promotion") will actually be performed | Assumption | Low | Major | ADR `:452` (R-3 row), `:675` (descoped note), `:526` (M-10, FM-010 "not yet instrumented" PR-template) | Actionability |
| IN-004-20260706 | The zero-governance null-alternative benchmark's "B beats the null" conclusion applies to the *current* (interim) state, not only the mature/enforced end-state | Assumption | Low | Major | ADR `:265` (IN-002-iter6 qualifier already present: "argued design advantage, not yet a demonstrated one") | Evidence Quality |
| IN-005-20260706 | The stated Confidence range (0.70-0.75) already accounts for lint-design completeness risk | Assumption | Low | Minor | ADR `:303` (Confidence section) | Traceability |

**Finding ID note:** execution_id `20260706` used per-run per template convention; IN-NNN sequence restarts at 001 for this independent lane per adv-executor protocol (S-013 prefix is authoritative from the loaded template's Identity section).

---

## Finding Details

### IN-001: The Deleted L-12 Allowlist Leaves "Pre-Adoption Grandfathered" Unenforceable — the Lint Will Misfire on Its Own Corpus [CRITICAL]

**Type:** Assumption
**Original Assumption:** The 5-rule core's L-1 (Grammar) row is scoped "(git-added/modified files; pre-adoption grandfathered)" (`adr-standards-rule-draft.md:171-179`; ADR `:663-672`), and the grandfather regression test asserts "the 18 files reachable by the scan path... pass L-1" (ADR `:672`; rule draft `:179`).

**Inversion:** Independently verify the claim by applying the two literal regexes to the actual corpus. Canonical: `^ADR-[a-z][a-z0-9]*(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$` (rule draft `:70`). Dialect: `^ADR-(PROJ|EPIC|FEAT|STORY)\d{3}-\d{3}(-[a-z0-9-]+)?\.md$` (rule draft `:71`). A live file in the scanned corpus, `projects/PROJ-030-bugs/decisions/ADR-150-001-pre-tool-enforcement-consolidation.md` (Glob-verified to exist, 2026-07-06), matches **neither**: its leading token `150` begins with a digit (excluded from canonical by design — the rule draft says so explicitly at line 70: "so `ADR-150-001` is not a canonical slug"), and `150` is not a member of the closed dialect prefix set `{PROJ|EPIC|FEAT|STORY}`. Yet both the ADR (`:223`, D-4: "16 live `ADR-PROJ*/EPIC*/STORY*/150` dialect ADRs") and the rule draft (`:94`, Frozen and Grandfathered Legacy: "Grandfathered dialect families (...`150`×1) remain valid in place, extendable within their dialect") repeatedly label it a **"dialect"** file — a taxonomic misstatement, since by the document's own ID Scheme it is neither canonical nor dialect; it is the unaddressed **GH-issue-scoped family** from the original 9-family corpus survey (ADR `:104`: "GH-issue scoped | `ADR-{issue}-NNN` | `ADR-150-001` | 1 | Origin (issue)").

The prior design (iterations 1-3) had a mechanism for exactly this problem: **L-12 "grandfather-allowlist freeze,"** which brought the allowlist "under the waiver ledger's audit discipline" (Changelog 1.3). The subtraction pass (FU.1) deleted L-12 outright, bundled with the waiver ledger, per its own deletion list: *"12 deleted outright (L-4b, L-5, L-6, L-6b, L-6c, L-8, L-9, L-10, L-11, **L-12**, L-13, L-14)"* (`subtraction-pass-notes.md:57`). L-12 was attack surface (a waiver-ledger-adjacent mechanism), so its deletion is consistent with the doctrine — **but nothing replaced the function it served**. The retained L-1/L-2 rule table's parenthetical "(...pre-adoption grandfathered)" is now pure prose with no data structure behind it: a git-based lint that scopes to "git-added/modified files" has no way to know that `ADR-150-001.md` predates adoption unless it is checked against *something* (a baseline commit reference, a hardcoded allowlist, or a snapshot manifest) — none of which exists in the retained 5-rule spec.

**Consequence:** The moment `ADR-150-001-pre-tool-enforcement-consolidation.md` is next `git`-modified for *any* reason (a typo fix, an `AMENDED` block per this very ADR's own new Amend-vs-Supersede convention, a `superseded_by` link added by a future ADR) — it re-enters the "git-added/modified" scope and:
- **L-1 (Grammar)** FAILS: matches neither regex.
- **L-2 (No new bare)** also risks a FALSE POSITIVE: the filename matches the bare-detection pattern `^ADR-\d` (ADR `:667`), so a 6-year-old grandfathered file could be flagged as "no new bare `ADR-NNN`" on a routine edit.

This directly contradicts the grandfather regression test's stated purpose — "the dry-run-against-the-real-corpus step whose absence caused an earlier lowercase-only defect" (ADR `:672`) — which exists *precisely* to catch this class of bug before shipping. The regression test as currently specified (run the 18 files through L-1 once, at build time) would not catch this, because the failure only manifests on a **future edit**, not on the initial dry run. This is a genuine "what would guarantee failure on day one" condition the S-013 protocol is designed to surface: the design, taken literally, is not internally consistent with its own grandfather promise for at least this one file, and the fix (re-adding some form of baseline/allowlist tracking) is exactly the kind of "compensating machinery" the subtraction doctrine says not to re-add — creating a genuine tension the package does not yet resolve.

**Plausibility:** High — this is not a hypothetical edge case; `ADR-150-001` already exists, is already cited from `.context/rules/quality-enforcement.md`-adjacent lineage (BUG-006 tournament work), and ADRs of its vintage are exactly the kind of file that accumulates `AMENDED` blocks or supersession links over time under the very Amend-vs-Supersede convention this package introduces.

**Confidence:** Low (that the assumption holds) / High (that the regexes and file both exist as cited — independently Glob/Read-verified).

**Dimension:** Methodological Rigor (design does not correctly implement its own stated behavior) and Completeness (the grandfather test's "18 files pass" claim is not accurate under a literal reading).

**Mitigation:** Either (a) narrow the claim — state plainly that the grandfather test validates *initial* dry-run pass only, and that any future edit to a non-canonical/non-dialect legacy file (the GH-issue-scoped and any other ungoverned family) will require a scoped exception, disclosed as a residual (R-14) rather than silently assumed away; or (b) add the minimum viable allowlist mechanism — not a ledger, just a static list of the (currently) 16 known-grandfathered filenames baked into the lint script at build time (M-6), which is a one-time data artifact, not standing machinery, and therefore consistent with the subtraction doctrine's "delete machinery, not necessary state." Recommend (b): it is the smallest fix that makes the existing claim true.

**Acceptance Criteria:** The Enforcement Design / L5 Lint Specification sections state explicitly how L-1/L-2 distinguish "grandfathered, exempt forever" files from "newly added" files when a grandfathered file is subsequently modified — either via a named static allowlist artifact or via an explicit, disclosed residual narrowing the "18 files pass L-1" claim to "18 files pass an initial dry run; future edits to non-canonical/non-dialect legacy files are a disclosed gap (R-14)."

---

### IN-002: The FM-5 "Nothing Lands" Scenario Is the Verified Present State, Not a Modeled Future Risk [MAJOR]

**Type:** Anti-Goal
**Original Assumption (implicit):** The Pre-Mortem row FM-5 ("It is 2026-12-31 and this decision has failed... M-2, M-6, and M-12 all stay untracked `TBD-Task`s... the convention is still visible only to a *reader* of this ADR") frames this as a probabilistic future scenario ("Severity: HIGH, Occurrence: MED-HIGH", ADR `:482`).

**Inversion:** Independently checked, as of **today** (2026-07-06, the date of this review, one day after the ADR's own "zero tracked work" disclosure of 2026-07-05):
- `.context/rules/adr-standards.md` — **does not exist** (Glob, this session: "No files found"). M-2 has not landed.
- `CLAUDE.md` Navigation table (`CLAUDE.md:51-63`) — lists `.context/rules/` generically (line 53) and three specific rule files by name (lines 54-56: `quality-enforcement.md`, `agent-development-standards.md`, `agent-routing-standards.md`). **No entry for any ADR-standards or ADR-convention rule exists.** M-7 (discretionary CLAUDE.md registration) has not landed either — consistent with the package's own "No (discretionary...)" gating note, but confirms the convention is invisible from the one file every session auto-loads.
- `projects/PROJ-031-cowork-skeleton/work/**` (Glob) — contains only unrelated `EPIC-001-skeleton-distribution` items; **zero** Task/Story/Enabler entities reference the ADR convention, M-2, M-6, M-9, or M-12.
- `skills/problem-solving/agents/ps-architect.md` — independently read: line 218 still emits bare `# ADR-{NUMBER}: {Title}`; line 260 still directs `Write` to `projects/${JERRY_PROJECT}/decisions/{ps_id}-{entry_id}-adr-{slug}.md` (a grammar matching **neither** the canonical nor dialect regex — it has no `NNN` sequence component and `{ps_id}` is not confined to the closed dialect prefix set); line 263 still cites the phantom `templates/adr.md`; lines 267-268 still invoke `python3 scripts/cli.py` (a nonexistent script, and a direct H-05 violation — `python3` instead of `uv run jerry`). M-12 has not landed.

**Consequence:** The condition FM-5 hedges as "HIGH severity, MED-HIGH occurrence" for **2026-12-31** is already fully satisfied **today**, five months early, and has not moved in the 24 hours since the package's own disclosure. This does not invalidate Scheme B, but it does mean the Status section's framing — "in force... this DESIGNED-vs-BUILT line is drawn plainly" (ADR `:89`) and Enforcement Design's "the guidance delivers value with zero tooling" — describes a value proposition that has not yet been realized for a single ADR authored through the normal agent-invocation path, because the one agent that authors ADRs neither knows about nor could comply with the convention if it tried.

**Plausibility:** Certain — independently verified, not inferred.

**Confidence:** High that the gap exists; the package itself already names most of these facts individually (M-2/M-7/M-12 rows), but frames the compound as a future pre-mortem narrative rather than a present, confirmed fact.

**Dimension:** Traceability (the FM-5 severity/occurrence framing should be updated to reflect confirmed-current rather than modeled-future) and, secondarily, Internal Consistency (the Status section's "in force" language and the FM-5 "it is 2026-12-31 and this has failed" framing are in tension when the triggering conditions are already true today).

**Mitigation:** Re-date FM-5 from a 2026-12-31 hypothetical to a dated, confirmed-as-of-2026-07-06 status note, and soften "in force" language in Status/Enforcement Design to something like "ratified and available to any reader of this file; not yet loaded, registered, or producer-enforced as of 2026-07-06" — this is a wording fix, not new machinery, fully consistent with the subtraction doctrine.

**Acceptance Criteria:** FM-5 (or a new dated status note) states the verified-current facts (no `.context/rules/adr-standards.md`, no CLAUDE.md entry, no tracked Task, producer unfixed) rather than a future-tense narrative, and the Status section's "in force" claim is qualified to the same degree the Migration Plan already qualifies M-2/M-12 individually.

---

### IN-003: The R-B Manual Citation-Sweep Mitigation Has No Trigger Mechanism — the Historical Failure Recurs by Default [MAJOR]

**Type:** Assumption
**Original Assumption:** Free-text/full-path/GitHub-Issue citation staleness (R-B) is mitigated by "a manual `grep`/`gh issue list` sweep... **owner: governance; cadence: at each Path-1/Path-2 promotion**" (ADR `:675`; rule draft `:197`).

**Inversion:** Ask what would guarantee this mitigation does not happen. Answer: exactly what already happened. The ADR's own headline motivating evidence is that the stale `ADR-PROJ007-001/002` citations have sat unrepaired for **2.5 months** after that promotion (ADR `:73`, `:256`; M-10 row `:526`), despite there being an obvious, well-known need to re-point them. "Owner: governance" does not bind to a specific person or agent role that is invoked at promotion time; "cadence: at each promotion" is not wired to any artifact — the PR-template checklist item that would make this checkable is itself disclosed as "intended, not yet instrumented" (FM-010, ADR `:525`, M-9 row). There is therefore **no structural difference** between the conditions that produced the 2.5-month-stale wound and the conditions under which the *next* promotion will occur. The package's own confidence framing treats this as a bounded, disclosed residual (R-B) rather than an active, undifferentiated repeat of the founding failure mode.

**Consequence:** The central motivating claim — "promotion becomes free" (ADR L0) — is free only for the ~72% bare-ID citation majority measured within `.context/rules/` (a scope explicitly flagged as non-generalizable, ADR `:554`). For the ~28%+ full-path/GH-Issue minority, and for any citation outside the narrow `.context/rules/` measurement corpus, nothing has changed about *why* the mitigation will actually run this time.

**Plausibility:** High — no counter-evidence exists that "governance" cadence commitments without a wired trigger are followed reliably; the one data point available (PROJ-007) shows the opposite.

**Confidence:** Medium — the package already discloses this residual in detail (more thoroughly than most conventions would); this finding's contribution is that "disclosed" is not the same as "mitigated," and the severity classification (currently folded into a LOW-probability risk row, R-1/R-B framing) understates the base rate given the one historical data point is a 100% failure.

**Dimension:** Actionability — the mitigation as stated is not concrete/verifiable per the S-013 rubric's own Actionability criterion.

**Mitigation:** Attach the sweep to a checkable, low-cost artifact that does not require new standing machinery: a single checklist line in the Promotion Process (Path 1 step 4 / Path 2 step 5) reading "author ran `grep -rl` for the old ID across `WORKTRACKER.md`, `*.yaml`, and issue titles before marking this promotion complete" — a self-attestation, not a gate, consistent with MEDIUM tier and adding zero enforcement machinery.

**Acceptance Criteria:** The next real promotion (Path 1 or Path 2) records, in its own PR description or Changelog entry, that the citation sweep was run and what it found — closing the loop between "disclosed residual" and "actually executed" for at least one instance.

---

### IN-004: The Null-Alternative Benchmark Answers the Mature-State Question, Not Today's Question [MAJOR]

**Type:** Assumption
**Original Assumption:** "The null alternative loses because it has neither [a free discovery substrate nor a collision/coherence story]... B is therefore, by design, better than the null" (ADR `:265`).

**Inversion:** The ADR itself already partly discloses this ("Qualifier (IN-002, iter-6, P-022): this 'better than the null' is an *argued design advantage, not yet a demonstrated one*... it is a well-reasoned prediction," `:265`). Stress-testing this qualifier against IN-001/IN-002/IN-003 above sharpens it: **today**, before M-2/M-6/M-9/M-12 land, Scheme B delivers (a) zero realized citation-stability benefit (zero Path-1 promotions have ever occurred, ADR `:579`), (b) zero realized discoverability benefit for agent-authored ADRs (the producer still emits non-compliant filenames), and (c) a real, non-zero taxonomy-governance and onboarding cost that begins accruing the moment anyone other than this review chain reads the file. The null alternative (do nothing; rely on `grep`/an index) has, today, an **identical realized benefit (zero)** at **lower cost (zero taxonomy governance, zero new ontology exception to learn)**.

**Consequence:** "B beats the null" is true of the intended end-state (once M-12 ships compliant IDs and M-2 makes the rule auto-loaded) but is not yet true of the state the package will actually be scored and operated in for an unknown period. Presenting the benchmark without this time-qualification risks the reader concluding the comparative advantage is already banked, when it is a forward claim resting on four still-open Migration Plan items.

**Plausibility:** High, and largely self-disclosed already (IN-002-iter6) — this finding's value is tying that existing disclosure explicitly to the newly-verified IN-002 facts above, so the "not yet demonstrated" qualifier is read as "confirmed not yet true," not merely "theoretically unconfirmed."

**Confidence:** Medium-High.

**Dimension:** Evidence Quality — the benchmark's evidentiary basis is a design argument, and should be labeled with the same rigor the package applies elsewhere (e.g., the Path-1 "designed default, not yet demonstrated" framing at `:579`) rather than "the null alternative loses" stated as a completed verdict at `:265`.

**Mitigation:** Add one sentence to the null-alternative section explicitly cross-referencing the current (not just future) cost/benefit balance, consistent with the honesty standard the rest of the document already holds itself to.

**Acceptance Criteria:** The null-alternative section states plainly that its "B beats the null" conclusion is conditioned on M-2/M-6/M-12 landing, and that in the interim state the comparison is a wash on realized benefit with a taxonomy-governance cost tilted toward the null.

---

### IN-005: Confidence Range Predates This Review's Lint-Design Finding [MINOR]

**Type:** Assumption
**Original Assumption:** Confidence 0.70-0.75 (ADR `:303`) is scoped to "a C4 governance flip resting on n=3" (the promotion-frequency belief).
**Note:** IN-001 (the L-12/grandfather gap) is a distinct axis — not about whether Scheme B is the right *decision*, but whether the *lint design* supporting it is complete. The existing confidence figure correctly does not need to move for the decision itself, but a forward note should distinguish "confidence in Scheme B" from "confidence the M-6 lint ships bug-free as specified," since this review found the latter is not yet true.
**Severity:** Minor — a labeling/scoping clarity issue, not a substantive risk.
**Dimension:** Traceability.
**Mitigation:** Add a one-line cross-reference from the Confidence section to the Enforcement Design section noting the two confidence axes are independent.

---

## Recommendations

**MUST mitigate (Critical):**
- IN-001-20260706: Add a static grandfather allowlist (data artifact, not new machinery) to the M-6 lint spec, or explicitly narrow the "18 files pass L-1" claim with a disclosed residual (R-14) covering future edits to non-canonical/non-dialect legacy files (`ADR-150-001` named specifically). Acceptance: Enforcement Design / L5 spec states how a grandfathered file surviving a future edit is distinguished from a newly-added bare file.

**SHOULD mitigate (Major):**
- IN-002-20260706: Reframe FM-5 from future-tense pre-mortem to a dated, confirmed-current-state disclosure; soften "in force" language in Status/Enforcement Design to match the Migration Plan's own honesty standard.
- IN-003-20260706: Attach the R-B citation sweep to a one-line self-attestation checklist item in the Promotion Process (no new gate, no ledger).
- IN-004-20260706: Add one sentence to the null-alternative section conditioning "B beats the null" on M-2/M-6/M-12 landing.

**MAY mitigate (Minor):**
- IN-005-20260706: Cross-reference the Confidence section to the Enforcement Design section to separate "decision confidence" from "lint-design completeness confidence."

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-001: the grandfather regression test does not actually cover the full retained corpus under a literal reading of L-1/L-2 |
| Internal Consistency | 0.20 | Negative | IN-002: "in force... delivers value with zero tooling" (Status/Enforcement Design) is in tension with the independently-verified current state; "150" is called "dialect" (ADR `:223`, rule draft `:94`) while not matching the dialect grammar (rule draft `:71`) |
| Methodological Rigor | 0.20 | Negative | IN-001: subtraction pass removed L-12 without replacing the function it served for the one non-canonical/non-dialect grandfathered family |
| Evidence Quality | 0.15 | Negative | IN-004: null-alternative "beats the null" stated as a settled verdict once (`:265`) despite the package elsewhere correctly hedging the identical claim (`:265` IN-002-iter6, `:579` Path-1) |
| Actionability | 0.15 | Negative | IN-003: R-B mitigation has an owner and a cadence but no trigger artifact |
| Traceability | 0.10 | Neutral-to-Negative | IN-005: two distinct confidence axes (decision vs. lint-design) are not distinguished; FM-5 severity/occurrence should reference confirmed-current evidence |

---

## Null-Alternative Reassessment

**Direct answer to the invoking question ("does it still beat the null alternative — no convention?"):** **In design, yes; in practice, not yet, and not by construction.** The package's own reasoning for why B beats a do-nothing/grep-and-index null (citation-integrity is the load-bearing failure; a self-describing filename is a free, always-current discovery substrate; the null externalizes cost onto every reader forever) is sound **once the convention is actually loaded, followed, and producer-enforced.** None of those three preconditions hold today (IN-002), the one repair mechanism for the founding failure mode (citation staleness) has no trigger (IN-003), and the enforcement design itself has an unaddressed edge case (IN-001). None of these three findings argue for reverting to the null — the design is still better *in kind* — but the honest, current-state answer is that the package has not yet banked the advantage it claims, and nothing in the post-subtraction package creates urgency or a forcing function to close that gap. This is consistent with, and sharpens, the package's own most self-critical language (IN-002-iter6, DA-003) rather than contradicting it.

---

## Execution Statistics
- **Total Findings:** 5
- **Critical:** 1
- **Major:** 3
- **Minor:** 1
- **Protocol Steps Completed:** 6 of 6 (goals stated, anti-goals inverted, assumptions mapped, stress-tested, mitigations developed, synthesized)
- **Independent verification performed:** Glob (`decisions/ADR-*.md` x2, `.context/rules/adr-standards.md`, `work/**`, `explore/*`), Read (`CLAUDE.md` full, `ps-architect.md:210-289`) — all citations in this report are either direct file:line quotes from the deliverable or independently re-verified facts, labeled as such.
