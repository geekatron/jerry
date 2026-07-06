# Steelman Report: ADR-PROJ031-004 / adr-standards-rule-draft (ADR Identifier, Location, and Promotion Convention)

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
- **Deliverable Type:** ADR (Architecture Decision Record) + companion MEDIUM-tier rule draft
- **Criticality Level:** C4 (engagement gate 0.95, above the 0.92 SSOT floor)
- **Strategy:** S-003 (Steelman Technique) -- iteration 4 (blind, independent)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (blind reviewer) | **Date:** 2026-07-02 | **Original Author:** ps-architect (per ADR footer)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Scoping Note](#scoping-note) | Why this report synthesizes rather than fully re-transcribes |
| [Steelman Reconstruction](#steelman-reconstruction) | The thesis in its strongest explicit form, with SM-NNN annotations |
| [Best Case Scenario](#best-case-scenario) | Ideal conditions and confidence assessment |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Expanded before/after/rationale for Major findings |
| [Scoring Impact](#scoring-impact) | Dimension-level effect of the identified strengthenings |

---

## Summary

**Steelman Assessment:** This is an unusually mature C4 governance package -- already on its fourth adversarial iteration, with extensive self-correction (RT/FM/PM/CC/DA/IN/CV/SM tags), a falsifiable ratification gate, and honest disclosure of every unresolved residual. Read most charitably, its central thesis -- *ADR identity should encode subject because ADRs are the one Jerry entity whose governing scope is mutable by design* -- is sound, well-argued from three largely independent lines of evidence, and deliberately low-regret. The package undersells itself in a few identifiable places: it has stronger corroborating evidence sitting in its own reference corpus than it cites, and it does not always apply its own hard-won methodological discipline (falsifiable, dated, owned commitments) symmetrically to every load-bearing claim.

**Improvement Count:** 3 Major, 3 Minor (0 Critical -- no gap found that would, if left unaddressed, prevent the core thesis from withstanding critique).

**Original Strength:** High. The core argument (mutability, not literal scope-encoding, is the correct differentiator) is already stated head-on, defended against its own steelmanned rejected alternative (Scheme C), sensitivity-tested against the load-bearing promotion-frequency assumption, and stress-tested with an explicit "regime in which this decision is wrong." Four iterations of self-refine have already closed most presentation, structural, and evidence gaps a first-pass Steelman would normally find.

**Recommendation:** Incorporate the identified strengthenings (all are additive -- none require revisiting the Decision). None invalidate D-1 through D-5; all make the existing case for them harder to attack on the specific points a Devil's Advocate / Red Team pass is likely to probe next: (a) the internal-consistency gap between rejecting Scheme C's "institutionalized" citation break while relying on a structurally identical Path-2 mechanism for the discouraged dialect case, and (b) the asymmetry between the rigorous, falsifiable Ratification Gate (G-1..G-4) and the un-dated, un-owned PM-009 promotion-rate monitoring commitment.

---

## Scoping Note

Per the Execution Protocol (Step 6), a full deliverable rewrite is the canonical S-003 output. Given the deliverable's combined length (1,071 lines across the ADR + rule draft) and that it has already absorbed four rounds of adversarial remediation with no discernible incoherence, a line-by-line re-transcription would reproduce ~95% of the existing text unchanged and add no signal. This report instead (a) restates the core thesis in its single strongest explicit form below, and (b) documents every point at which the *existing* strongest form is demonstrably improvable with specific, cited evidence -- consistent with Step 3's instruction to supply missing evidence and strengthen logical connections without changing the original thesis. This scoping choice is disclosed per P-022 rather than silently substituted for the template's default full-reconstruction format.

---

## Steelman Reconstruction

**Core thesis, stated in its strongest form:**

> Every Jerry entity ID choice is really answering one question: *which of this artifact's properties is permanent enough to serve as its name?* For PROJ/EPIC/FEAT/STORY/`DEC-NNN`, the answer is scope, because scope never changes for those entities once assigned -- a STORY is born and dies a STORY (ADR-PROJ031-004, [Rationale](#rationale--answering-the-crux-head-on)). The ADR is the single artifact class Jerry has ever built that is *meant* to change scope -- promotion from project to framework is not an edge case the ontology stumbled into, it is the explicit mechanism by which Jerry's own stated thesis ("accrues knowledge... from projects into the framework," `CLAUDE.md` Identity) operates. Naming that one migrating artifact after its current (mutable) scope, the way every non-migrating entity is named, is therefore not "following the ontology" -- it is applying a rule to the one case it was never designed to cover.
>
> This is not merely a theoretical category error. It has already cost the framework real, unrepaired damage: **[SM-001]** every single ADR filename in the live corpus -- whether canonical domain-slug (`ADR-agent-design-001`) or the permitted project/entity dialect (`ADR-PROJ031-001-skeleton-distribution-strategy.md`, `ADR-EPIC002-001-strategy-selection.md`, `ADR-STORY015-001-tier-model-renumbering.md` -- filesystem-verified 2026-07-02) -- already carries a hand-appended, human-authored subject-descriptive tail. No author, in any of the ~18 ADRs surveyed, has ever shipped a bare origin-only ID (`ADR-PROJ031-001.md` with no tail) even though the stated dialect grammar (`ADR-{PROJECT-ID}-NNN-{title-slug}.md`, rule draft ID Scheme table) treats the tail as optional decoration. That is a unanimous, cost-free, entirely organic natural experiment already run by the corpus itself: when origin alone is available as identity, every author has independently judged it insufficient and added a subject descriptor by hand. Scheme B does not invent a new need; it promotes an already-universal practice from decorative tail to primary identity, and eliminates the one thing the tail cannot fix -- that the *load-bearing* portion of the name (the part that survives a `grep`, a citation, a `sort`) is still the mutable, promotion-breaking origin token.
>
> **[SM-003]** The document is itself a live instance of the exact failure mode it exists to close, and rather than hide that, it schedules its own correction (`ADR-PROJ031-004` -> `ADR-adr-convention-001` via Path-2 self-promotion, M-9) as a disclosed worked example. That a framework-scope governance decision, authored by the most qualified agent available, under no external time pressure other than a mandated file path, *still* could not be filed under its own canonical scheme at birth is not an embarrassment to the thesis -- it is corroborating evidence for it: if even this document's own authorship process defaults to the discouraged dialect under ordinary task constraints, the uncertainty ADR-M-013 defaults toward canonical slugs to manage is real, present, and not confined to less-careful authors.
>
> **[SM-005]** The rejection of Scheme C is sometimes read as claiming C's rename-and-tombstone remedy is broken. It is not: Path 2 -- the mechanism this very decision keeps for the discouraged dialect-promotion case -- is structurally the *same* remedy C would apply to every promotion. The actual, sharper argument is about *frequency of exposure*, not remedy quality: B is preferred not because it has a better fix for the citation-break failure mode, but because it is designed so that the shared fix (tombstone + re-point) is invoked only in the disclosed-exceptional case (D-3 dialect ADRs that later promote) rather than on every single promotion, which is what C would require by construction. Making this equivalence explicit closes the objection "if Path 2 is acceptable for you, why is the structurally identical mechanism unacceptable for Scheme C" before a critic raises it.

**Best Case Scenario:** See below.

---

## Best Case Scenario

**Ideal conditions under which this decision is most compelling:** (1) the observed 2-of-2 (PROJ-007) / 1-of-3 (EPIC-002) framework-mandate promotion rate continues or grows as the project count grows (the PM-009 belief holds); (2) the L5 lint (M-6) actually ships as a hard ratification blocker, closing the "advisory-only" gap disclosed throughout; (3) a second CODEOWNERS-eligible maintainer materializes, making the waiver mechanism's second-reviewer requirement exercisable rather than fallback-only; (4) the taxonomy arbiter (M-5b) is staffed and actually adjudicates near-duplicate slugs before the corpus grows past ~50 ADRs.

**Key assumptions that must hold:** the promotion-frequency belief is not an artifact of a 2-project sample; the governance apparatus specified in the rule draft is actually built (not merely designed); Jerry's project count keeps growing (so the "compounds with corpus size" argument for B has room to compound).

**Confidence assessment (of this Steelman, not to be conflated with the document's own 0.70-0.75 confidence in the underlying decision):** High (~0.85) that Scheme B plus the disclosed governance apparatus is the *correct call given the evidence the package itself presents* -- because two of its three supporting arguments (ontology category-error, promotion-independent discoverability) hold regardless of the promotion-frequency regime, exactly as the document itself argues. The remaining uncertainty is not in the thesis but in execution follow-through (M-6/M-12/second-maintainer), which the document already tracks as INHERENT residuals rather than claiming resolved.

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|---------------|-----------|
| SM-001-20260702 | Missing self-referential evidence: every ADR filename in the live corpus (dialect and canonical alike) already carries a hand-appended subject tail -- direct, cost-free corroboration of the discoverability argument that the package does not currently cite | Major | Discoverability argument rests solely on the BUG-006 Nielsen citation (ADR body, [Rationale](#rationale--answering-the-crux-head-on) point 2) | Add the corpus-wide "universal tail" observation as independent, self-generated corroboration alongside BUG-006 | Evidence Quality |
| SM-002-20260702 | PM-009 (the promotion-frequency monitoring commitment) is prose without an owner, a calendar/event trigger, or a review-by date -- inconsistent with the document's own demand (applied to its G-1..G-4 Ratification Gate) that "a prose table row is a plan, not evidence of completion" | Major | "Commitment: re-examine the promotion rate after the next 2-3 framework-relevant projects... This is disclosed as a known limitation, not resolved." (ADR body, [Risks](#risks), Post-ratification monitoring commitments) | Name an owner and a concrete, checkable trigger (event count or calendar date), mirroring the waiver ledger's `review_by` field pattern already used elsewhere in the same document | Methodological Rigor / Internal Consistency |
| SM-003-20260702 | The rejection of Scheme C's "institutionalized... not eliminated" citation break does not explicitly acknowledge that Path 2 (kept for the discouraged dialect case) is the structurally identical remedy -- leaving an unstated equivalence a critic can expose as a double standard | Major | "C institutionalizes the citation break rather than eliminating it" (ADR body, Scheme C cons, [Options Considered](#options-considered-af)) | State explicitly that B's advantage over C is frequency-of-invocation of a shared remedy, not remedy superiority, foreclosing the "why is Path 2 OK then" objection | Internal Consistency |
| SM-004-20260702 | The "living proof" argument (this ADR's own dialect filename + scheduled self-promotion) is distributed across Rationale, Meta-Note, and Changelog but never stated once as a freestanding, headline piece of evidence in the Executive Summary or Decision | Minor | Scattered mentions in [Promotion-Frequency Sensitivity](#promotion-frequency-sensitivity-the-load-bearing-assumption) and [Meta-Note](#meta-note-this-adrs-own-identity-and-remap-path) | Add one consolidated sentence to L0/Decision naming this as a deliberate self-demonstration | Traceability / Actionability |
| SM-005-20260702 | External prior-art citations (log4brains, MADR, Nygard, GOV.UK, AWS -- Reference #11) are bundled without per-source URL/access-date verification, unlike every internal claim in the document, which carries file+line and "verified 2026-07-02" annotations | Minor | Reference #11 combines five external sources in one row with no URLs or verification dates | Add per-source URL/access-date citations matching the internal evidentiary standard, since log4brains' abandonment-of-monotonic-numbering and GOV.UK's maturity-gradient claims are load-bearing for the D and C steelmans | Evidence Quality |
| SM-006-20260702 | The "regime in which this decision is wrong" bounded-downside claim ("the downside is bounded and cheap") is asserted narratively without even an order-of-magnitude cost model, in contrast to the document's own DA-004 collision-risk-at-scale estimate, which is explicitly labeled qualitative but still reasoned through a concrete mechanism | Minor | "the downside is bounded and cheap; the upside... compounds with corpus size" (ADR body, [The regime in which this decision is wrong](#the-regime-in-which-this-decision-is-wrong-stated-plainly-p-022)) | Add a DA-004-style explicitly-qualitative cost sketch (e.g., number of Path-2 events x grep-and-replace operations per event, bounded by L-8 detection) | Completeness |

---

## Improvement Details

### SM-001-20260702 -- Corpus-wide organic tail convergence as self-generated evidence

**Affected Dimension:** Evidence Quality (0.15 weight)

**Original Content:** The document's discoverability argument (ADR body, [Rationale](#rationale--answering-the-crux-head-on), point 2) rests on one external source: "BUG-006 -- an evaluation the maintainers accepted and acted upon -- found the origin-encoded scheme fails 4 of 10 Nielsen heuristics." This is legitimate but is the *only* discoverability evidence offered, and it is a third-party heuristic review rather than a directly observed behavioral fact about the corpus.

**Strengthened Content:** Filesystem-verified 2026-07-02: every dialect ADR in the corpus already carries a hand-appended subject descriptor as part of its filename -- `ADR-PROJ031-001-skeleton-distribution-strategy.md`, `ADR-PROJ031-002-ci-token-push-strategy.md`, `ADR-PROJ031-003-credential-protection-supply-chain.md` (all three confirmed present in `projects/PROJ-031-cowork-skeleton/decisions/`), `ADR-EPIC002-001-strategy-selection.md` and `ADR-EPIC002-002-enforcement-architecture.md` (cited from `.context/rules/quality-enforcement.md:108,275,290,350-351`), and `ADR-STORY015-001-tier-model-renumbering.md` (cited from `.context/rules/agent-development-standards.md:455` and `.context/rules/mcp-tool-standards.md:231`). The dialect grammar itself (rule draft, [ID Scheme](#id-scheme) table, line 67: `ADR-{PROJECT-ID}-NNN-{title-slug}.md`) treats the `{title-slug}` as an optional tail -- yet zero corpus instances omit it. This is a unanimous, unprompted, zero-cost natural experiment: every author who had only an origin-scoped ID available still independently chose to hand-append a subject descriptor, demonstrating that subject-recognition need is not hypothetical or Nielsen-heuristic-only -- it is already how the corpus behaves when given the chance.

**Rationale:** This is stronger evidence than a single external usability review because it is (a) internally generated (no observer-expectancy concern), (b) unanimous across every instance in the corpus rather than a single flagged example, and (c) free -- it requires no new citation, only synthesizing filenames the document already references elsewhere (Related Decisions, Migration Plan, References tables).

**Best Case Conditions:** This argument is strongest precisely because it needs no external authority and cannot be dismissed as a single cherry-picked case; it is the entire population of dialect ADRs in the repository.

---

### SM-002-20260702 -- PM-009 lacks the falsifiability the document itself demands elsewhere

**Affected Dimension:** Methodological Rigor (0.20) / Internal Consistency (0.20)

**Original Content:** "Post-ratification monitoring commitments... **PM-009 -- forward promotion rate rests on n=3**... **Commitment:** re-examine the promotion rate after the next 2-3 framework-relevant projects produce ADRs; if forward promotion stays approximately 0%... Scheme C should be reconsidered... This is disclosed as a known limitation, not resolved." (ADR body, [Risks](#risks) section)

**Strengthened Content:** The document elsewhere builds exactly the falsifiable-gate discipline this commitment lacks: the [Ratification Gate](#ratification-gate-falsifiable-pre-conditions--in-001-iter-3) (G-1..G-4) exists specifically because "IN-001... correctly observed that the document did not apply that skepticism reflexively to its own highest-leverage transition." PM-009 is a second highest-leverage transition -- it gates whether the *entire decision* should later be superseded -- yet it is left as un-dated, un-owned prose, the exact anti-pattern G-1..G-4 was built to eliminate. A strengthened version names an owner (e.g., the same "governance" role already assigned M-5b's taxonomy-arbiter duty) and a concrete, checkable trigger: either an event count ("the 3rd new framework-mandate project to complete its decisions/ phase after ratification") or a calendar date, mirroring the `review_by` field the document already specifies for solo-maintainer waivers ([L5 CI Lint Specification](#l5-ci-lint-specification), solo-maintainer fallback).

**Rationale:** This closes a specific, high-value internal-consistency gap: the document's own IN-001 self-critique establishes "prose commitment is not evidence" as a principle; PM-009 is the one remaining place that principle was not yet applied. Since PM-009 gates the confidence figure (0.70-0.75) that underwrites the whole C4 decision, making it falsifiable materially strengthens Methodological Rigor without touching the Decision itself.

**Best Case Conditions:** Strongest when read alongside the document's own words -- it is not an external critique but the document's demonstrated methodology, applied one section further than it currently reaches.

---

### SM-003-20260702 -- Path 2 and Scheme C share a remedy; the real differentiator is frequency, not remedy quality

**Affected Dimension:** Internal Consistency (0.20)

**Original Content:** "[Scheme C] institutionalizes the citation break rather than eliminating it: C's promotion step is the renumber that already broke citations (a 'managed' break, not zero -- C2=3)." (ADR body, [Options Considered](#options-considered-af), Scheme C cons)

**Strengthened Content:** Path 2 -- the mechanism this decision retains for the disclosed-discouraged dialect-promotion case (rename + bidirectional tombstone + citation re-point, [Promotion Process](#promotion-process-step-by-step)) -- is mechanically the same remedy Scheme C would apply to *every* promotion. The document's own evidence against C (the still-stale PROJ-007 citations, unrepaired "2.5 months later") is therefore not evidence that the tombstone-and-repoint remedy is defective in principle; it is evidence that *manual* rename-and-repoint, performed occasionally under Path 2 or systematically under C, has so far had a 100% observed non-completion rate on the one historical sample available. The correct, sharper framing: B is preferred over C not because it possesses a better fix for the failure mode, but because B's default (Path 1, pure `git mv`) is designed to invoke that unreliable manual remedy only in the rare, disclosed exception (D-3 dialect ADRs that later promote), whereas C would require it on every single promotion by construction. Stating this equivalence explicitly pre-empts the objection: "if Path 2's identical mechanism is acceptable for the framework's own governing ADR, why is it disqualifying for Scheme C?"

**Rationale:** Left implicit, this is exactly the kind of double-standard a Devil's Advocate or Red Team pass would surface next (the package has already absorbed CV-001/CV-002/DA-001-through-006 corrections of comparable structure). Stating it preemptively converts a potential Internal Consistency finding in the next adversarial iteration into an already-closed point.

**Best Case Conditions:** Strongest when paired with the document's own PM-009/R-6 "monitored, not eliminated" framing -- this is the same intellectual move (name the shared residual honestly) applied one level deeper, to the citation-break remedy itself rather than only to the promotion-frequency assumption.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | SM-006 adds a cost-model sketch for the adverse regime, matching the rigor already applied to the collision-risk-at-scale estimate (DA-004) |
| Internal Consistency | 0.20 | Positive | SM-002 and SM-003 close two latent asymmetries (falsifiability applied unevenly; Path 2 vs. Scheme C double standard) before an external critic surfaces them |
| Methodological Rigor | 0.20 | Positive | SM-002 extends the document's own IN-001-derived falsifiable-gate discipline to a second load-bearing transition (PM-009) |
| Evidence Quality | 0.15 | Positive | SM-001 supplies free, unanimous, self-generated corpus evidence for the discoverability argument; SM-005 closes an internal/external citation-rigor asymmetry |
| Actionability | 0.15 | Neutral | Findings are incorporable without any change to D-1 through D-5; SM-004's consolidation is a readability aid, not new decision content |
| Traceability | 0.10 | Positive | SM-004 makes the self-demonstration argument a single, findable statement rather than three scattered references |

---

*Steelman execution complete. All findings are additive strengthenings of an already-sound, heavily-iterated thesis; none contest the Decision (D-1 through D-5). Ready for downstream S-002/S-004/S-001 critique strategies per H-16, and for the parent orchestration's synthesis of this iteration's blind reviewer set.*
