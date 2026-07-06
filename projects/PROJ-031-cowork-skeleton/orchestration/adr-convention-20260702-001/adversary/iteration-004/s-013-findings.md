# Inversion Report: ADR Identifier, Location, and Promotion Convention (ADR-PROJ031-004 + companion rule draft)

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverables, blind-protocol scope |
| [Goal Inventory](#goal-inventory-step-1) | Explicit and implicit goals extracted |
| [Anti-Goal Analysis](#anti-goal-analysis-step-2) | What would guarantee failure, and whether the package does it |
| [Assumption Map](#assumption-map-step-3) | Explicit/implicit assumptions with confidence and validation status |
| [Findings Summary](#findings-summary) | All findings, severity-classified |
| [Detailed Findings](#detailed-findings) | Full evidence, analysis, mitigation per finding |
| [Zero-Governance Null-Alternative Re-Benchmark](#zero-governance-null-alternative-re-benchmark) | Inverted-goal comparison requested by the invoking task |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Totals |

---

## Execution Context

- **Strategy:** S-013 (Inversion Technique)
- **Template:** `.context/templates/adversarial/s-013-inversion.md`
- **Deliverables:**
  - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (759 lines)
  - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (312 lines, companion MEDIUM-tier rule draft)
- **Criticality:** C4. Engagement quality gate: 0.95 (raised above SSOT 0.92).
- **Iteration:** 4. Prior iterations (1-3) each ran full adversarial rounds (scores 0.67, 0.54, 0.62 per the ADR's own Changelog); iteration 4 so far shows only a narrower S-010 self-refine remediation pass in the Changelog.
- **Blind protocol:** This execution did NOT read any file under `.../adversary/` other than this output file. No prior iteration's findings were consulted. Any overlap with prior review tags embedded in the deliverable (`IN-NNN`, `CV-NNN`, etc.) is coincidental convergence, not copying — this executor's own `IN-NNN` identifiers below are assigned independently for this iteration.
- **H-16 status:** The deliverable's own text asserts S-003 Steelman has been applied throughout (each Option A-F carries an explicit steelman). Treated as satisfied per the deliverable's self-report; not independently re-verified (out of scope for S-013).

---

## Goal Inventory (Step 1)

| # | Goal (restated, specific/measurable) | Explicit/Implicit |
|---|---------------------------------------|--------------------|
| G-1 | Give every future ADR a stable, subject-encoded identifier (`ADR-{domain-slug}-NNN`) that never changes across the ADR's lifecycle, including promotion from project to framework scope. | Explicit (D-1, D-2) |
| G-2 | Make project→framework promotion a zero-citation-churn `git mv` (Path 1) for canonical ADRs, eliminating the demonstrated citation-break failure mode (BUG-006, stale `ADR-PROJ007-001/002`). | Explicit (D-2, Decision) |
| G-3 | Preserve provenance (birth project/entity) without encoding it in identity, via frontmatter. | Explicit (D-1, ADR-M-002) |
| G-4 | Introduce the convention as MEDIUM-tier only (no new HARD rule), deterministically lint-enforced, without spending a HARD Rule Ceiling Exception slot. | Explicit (D-5, c-001/c-002) |
| G-5 | Avoid big-bang renumbering; grandfather all 16 existing dialect ADRs in place. | Explicit (D-4, c-003) |
| G-6 (implicit) | Actually get ratified (`PROPOSED` → `ACCEPTED`) and adopted by future ADR authors and the ADR-producing agent (`ps-architect.md`) in a reasonable timeframe, so the convention is a living practice rather than a permanently-aspirational document. | Implicit (necessary for G-1..G-5 to have any real-world effect) |
| G-7 (implicit) | Achieve engagement-quality-gate ratification (>= 0.95) through a remediation process that converges, not one that merely accretes bulk. | Implicit (necessary given H-13/H-14 and the stated 0.95 gate) |

**Completeness check:** G-6 and G-7 are goals the deliverable clearly needs but never states as goals in its own [Purpose]/[Decision] language — it treats "ratification" and "adoption" as downstream administrative steps (Migration Plan) rather than as goals to be inverted and stress-tested in their own right. This gap is itself the seed of several findings below (IN-001, IN-007).

---

## Anti-Goal Analysis (Step 2)

For each goal, "what would guarantee failure?" — and whether the package currently does that thing.

| Goal | Anti-goal condition (guarantees failure) | Does the package do this? |
|------|-------------------------------------------|------------------------------|
| G-1 (stable identity) | Allow the identifier grammar to be ambiguous or allow multiple lint-passing families to silently collide. | No — L-1a/L-1b split + L-2/L-3 address this directly. Addressed. |
| G-2 (zero-churn promotion) | Never actually exercise Path 1; keep coupling promotion to a rename. | Partially present as a **disclosed** residual (DA-003: "zero Path-1 promotions have actually occurred yet," ADR:547) — honestly named, not hidden. Not a new finding. |
| G-3 (provenance) | Make provenance presence-only, never accuracy-checked, so a stale/copied value is indistinguishable from a correct one. | **Yes, partially** — L-6 is presence-only; L-6b (accuracy) is WARN and "best-effort... skipped where origin is not derivable" (ADR:654). This is disclosed (FM-104) but the residual gap remains real. Already disclosed; not re-flagged as a new finding. |
| G-4 (stay MEDIUM, no HARD spend) | Design an enforcement mechanism whose FAIL rules are *practically* non-overridable for the actual repo topology. | **Yes — see IN-005.** The solo-maintainer waiver fallback, meant to fix this, reintroduces a different but equally consequential defect (self-certifiable override). |
| G-5 (no big-bang) | Base the "no big-bang" grandfather promise on corpus counts that keep changing across iterations, so the regression-test fixture (G-2 ratification gate) itself is unverifiable-by-construction until the (nonexistent) lint is run. | **Yes — see IN-008.** |
| G-6 (ratify + adopt) | Couple ratification to completing nearly every item in a 14-row migration plan (new CI lint w/ 12 rules, YAML parser, waiver ledger, CODEOWNERS integration, 3 separate downstream file fixes, worktracker scaffold docs) as a single all-or-nothing gate. | **Yes — see IN-001 (Critical).** This is the most consequential anti-goal match found. |
| G-7 (converging remediation) | Respond to each adversarial round by adding more disclosure/caveat/correction prose layered onto the same document, without reducing the surface area a fresh reviewer must re-verify, and without the score trend showing convergence. | **Yes — see IN-007.** |

---

## Assumption Map (Step 3)

| ID | Assumption | Explicit/Implicit | Confidence | Validation Status |
|----|------------|--------------------|------------|--------------------|
| A-1 | The waiver-ledger + API-verified-approver mechanism provides materially stronger override rigor than an unaudited inline comment, for Jerry's actual (single-maintainer) operating reality. | Implicit (load-bearing for the whole Enforcement Design section) | Medium (asserted, not tested) | Contradicted by the document's own PM-102 disclosure once traced to its logical end — see IN-005 |
| A-2 | Coupling "accept this naming guidance" to "complete the full engineering build-out" is a proportionate, low-risk ratification design for a MEDIUM-tier convention. | Implicit | Low | Not tested; contradicts the document's own admission (R-5: "Lint never gets built... HIGH" impact) — see IN-001 |
| A-3 | The `scope:` frontmatter field, once declared "mandatory... at authoring time" in prose (ADR-M-013), meaningfully reduces the risk of authors mis-classifying framework-vs-project intent. | Explicit | Low | Unvalidated — no FAIL-class lint enforces the field's presence at all — see IN-004 |
| A-4 | The requested zero-governance null-alternative benchmark (search/index vs. the winning scheme) covers the space of credible low-governance alternatives. | Implicit | Medium | Incomplete — a credible middle option (tag-registry, zero ID convention) is absent from the benchmark — see IN-002, IN-003 |
| A-5 | The Frontmatter Schema as published is complete and self-consistent with what this ADR's own header actually uses. | Implicit | Medium | Contradicted by the document's own frontmatter — see IN-006 |
| A-6 | The iterative "patch-in-place with disclosure blocks" remediation strategy is converging toward the 0.95 gate. | Implicit | Low | Not supported by the score history embedded in the document's own Changelog (0.67 → 0.54 → 0.62) — see IN-007 |
| A-7 | Manual, iteration-by-iteration filesystem counting of the grandfathered ADR corpus (11→16, 14→15, "~6"→11 lines) is now stable and will match whatever fixture the (unbuilt) L-1 regression test encodes. | Implicit | Low-Medium | Repeatedly falsified across iterations 1-4 by the document's own recount corrections — see IN-008 |
| A-8 | Prose guidance ("SHOULD be preserved unchanged," "discouraged") is sufficient to prevent title-slug churn during promotion without a corresponding lint check. | Explicit | Low | Untested; no FAIL rule exists for this — see IN-009 |

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| IN-001-i4 | Critical | Ratification gate couples cheap documentation value to an all-or-nothing 14-item engineering build-out, near-guaranteeing indefinite non-ratification | Status / Ratification Gate; Migration Plan |
| IN-002-i4 | Major | Requested zero-governance null-alternative benchmark omits a credible middle option (tag-based registry, zero ID convention) | Zero-governance null alternative |
| IN-003-i4 | Major | The "an index is itself governance" objection used to reject the null is applied inconsistently — Scheme B's own taxonomy arbiter is a heavier ongoing governance burden | L2 Architectural Implications; Migration Plan M-5b |
| IN-004-i4 | Major | `scope:` frontmatter declared "mandatory at authoring time" has zero FAIL-class lint enforcement | ADR-M-013 (rule draft); Promotion-Frequency Sensitivity; L5 Lint Spec |
| IN-005-i4 | Major | Solo-maintainer waiver fallback reintroduces the exact self-certification weakness the audited-ledger redesign (RT-004) was built to eliminate | Solo-maintainer reality and waiver fallback |
| IN-006-i4 | Major | `canonical_id` field used in this ADR's own frontmatter is absent from the Frontmatter Schema the convention itself defines | Frontmatter (both files) |
| IN-007-i4 | Major | Cross-iteration score trend (0.67→0.54→0.62) embedded in the Changelog does not support the assumption that the patch-in-place remediation strategy is converging toward the 0.95 gate | Changelog |
| IN-008-i4 | Major | Recurring, self-disclosed corpus-count corrections across iterations (11→16; 14→15; ~6→11 lines) undermine confidence in the manually-verified counts the unbuilt G-2 regression test will depend on | D-4; M-14; Migration Plan; L-1 regression test |
| IN-009-i4 | Minor | Title-slug preservation during Path-1 promotion is guidance-only ("SHOULD," "discouraged") with no corresponding lint rule | Promotion Process Path 1 |

---

## Detailed Findings

### IN-001-i4: Ratification gate bundles cheap guidance-value with an all-or-nothing engineering build-out [CRITICAL]

**Type:** Anti-Goal (G-6: ratify + adopt)
**Original assumption (A-2):** Coupling "accept this naming guidance" to "complete the full engineering build-out" is a proportionate ratification design.
**Inversion:** To guarantee this MEDIUM-tier naming convention never actually takes effect, make `PROPOSED → ACCEPTED` conditional on completing nearly the entire migration plan as a single bundle.
**Evidence:** The Ratification Gate (`ADR-PROJ031-004-adr-identifier-convention.md:83-97`) states `status: PROPOSED` MUST NOT flip until G-1..G-4 are all TRUE, and G-4 explicitly reads: "Every gating Migration-Plan row (M-2..M-14 flagged 'Yes') has a real, linked, closed worktracker Task + GH Issue — not a `TBD` placeholder" (`:94`). Cross-checking the Migration Plan's own "Gating?" column (`:491-508`): of the 14 action rows (M-1 through M-14), **12 are marked "Yes"** (M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-11, M-12, M-13, M-14) and only **2 are "No"** (M-2b, M-10). The gating set includes: implementing and wiring a 12-rule CI lint with a novel YAML parser, an audited waiver ledger, and CODEOWNERS/branch-protection integration (M-6); fixing three separate downstream files — the exemplar template, `skills/architecture/SKILL.md`, and the ADR-producing agent `ps-architect.md` (M-3, M-4, M-12); retrofitting YAML frontmatter onto multiple existing framework and entity-dialect ADRs (M-11); documenting the worktracker scaffold (M-14); running a full `/adversary` C4 review of the ratified standard (M-8); and executing this ADR's own Path-2 self-promotion (M-9). Zero of these gating items currently exist as worktracker Tasks or GitHub Issues (`:489`, "As of 2026-07-02, **zero** worktracker Task entities and zero GitHub Issues exist for any Migration-Plan row").
**Plausibility:** High. The document itself independently names the corresponding risk — R-5 ("Lint never gets built; convention stays advisory-only," Probability MED, Impact HIGH, `:444`) and FM-1 in the Pre-Mortem ("The L5 lint was never implemented; the convention stayed a suggestion," `:461`) — but the stated mitigation for both is "M-6 is now a ratification blocker" (`:444`), which is the *cause* of the risk this finding identifies, not a fix for it: making the lint (and 11 other engineering items) a hard precondition for ratification does not make the lint more likely to be built by a solo maintainer with competing priorities; it only guarantees that if the lint stalls, the *entire* convention — including the parts that need zero tooling and could help authors today (the naming grammar itself, the promotion process, the amend-vs-supersede rules) — also stays unratified indefinitely.
**Consequence:** The convention's actually-useful, zero-cost part (documented naming/location/promotion guidance any human author could follow tomorrow) is held hostage to the completion of the expensive part (a from-scratch, YAML-parsing, 12-rule, audited-waiver CI lint plus three separate agent/skill fixes). Given the single-CODEOWNERS-identity reality the document itself verifies (`:637-638`, "`.github/CODEOWNERS`... assigns every governed path to the single identity `@geekatron`"), this bundle is unlikely to clear in any near-term timeframe, so the convention risks permanent `PROPOSED` status — precisely the FM-1/R-5 failure mode, but caused by the ratification design itself rather than merely a risk external to it.
**Dimension:** Actionability (0.15); secondarily Methodological Rigor (0.20)
**Mitigation:** Decouple ratification into at least two tiers: (a) **Tier 1 — guidance ratification**: adopt the naming/location/promotion/amend-vs-supersede rules as ACCEPTED MEDIUM guidance immediately upon user approval (G-1 only), since this requires no tooling and can start delivering value (and stopping new bare-`ADR-NNN` authorship by convention alone) right away; (b) **Tier 2 — enforcement ratification**: keep the CI lint, waiver ledger, and agent fixes (M-6, M-11, M-12, M-13) as a separately-tracked, non-blocking enforcement milestone that upgrades the guidance from advisory to lint-enforced once complete, without holding the guidance itself hostage.
**Acceptance Criteria:** The ADR's Status/Ratification Gate section is revised to specify a two-tier ratification model, OR an explicit, reasoned justification is added for why guidance-only ratification is unacceptable (e.g., citing a specific harm from advisory-only naming guidance that the current design does not already accept elsewhere, given the document's own repeated "advisory until M-6" framing for individual lint rules).

---

### IN-002-i4: Zero-governance null-alternative benchmark omits a credible middle option [MAJOR]

**Type:** Anti-Goal (inverted goal: "maximum decision-findability with zero governance")
**Original assumption (A-4):** The requested null-alternative benchmark (`ADR-PROJ031-004-adr-identifier-convention.md:263-269`) covers the credible space of low-governance alternatives.
**Inversion:** Invert the goal precisely as the invoking task requested: if the aim were *maximum decision-findability with zero governance*, what is the strongest low-governance design, and does the package's null-alternative section actually consider it?
**Evidence:** The "zero-governance null alternative" section (`:263-269`) frames the choice as a binary: Scheme B (the winning convention, with its full ID-grammar + 12-rule lint + waiver ledger + taxonomy arbiter apparatus) versus **total absence of any convention plus ad hoc grep/semantic search**. It does not consider a third option: **retain every existing ADR filename completely untouched (zero renames, zero grammar enforcement of any kind), and add only a lightweight, machine-generated registry keyed on frontmatter tags** (e.g., a `subject:` or `tags:` field, plus the already-proposed `origin_project`), regenerated by a trivial script (or even a WARN-only lint) that requires no filename convention, no L-1/L-2/L-3/L-4/L-9/L-12 filename-grammar rules, and no rename-triggering promotion path at all — because nothing is ever renamed, citation stability (the document's own stated decisive property, `:222` "This is the decisive property and the direct dissolution of the crux") is achieved automatically and for free.
**Plausibility:** High. This option is a strict evolution of what the document already partially concedes: the null-alternative's "why it still loses to B" argument (`:268`) rests entirely on citation-integrity and collision-avoidance, both of which a tag-registry-without-renaming option achieves at least as well as B (better on citation-integrity, since literally zero filenames ever change, versus B's still-real Path-2 rename case for anything currently under the discouraged dialect).
**Consequence:** The benchmark, as published, is not a fair test of "zero/minimal governance vs. this specific convention" — it compares the winning scheme only against a strawman (truly zero effort, uncurated grep) rather than against the strongest low-governance competitor. This weakens the Completeness and Evidence Quality of the requested inversion analysis, and means the confident conclusion "the benchmark confirms a convention is warranted; it does not favour doing nothing" (`:269`) is not fully earned — it is earned against the strawman, not against the credible middle alternative.
**Dimension:** Completeness (0.20); Evidence Quality (0.15)
**Mitigation:** Add the tag-registry-without-renaming option as a genuine third comparator (perhaps "Scheme G" or an explicit null-alternative variant) in the Options Considered and/or the null-alternative section, score it against the same C1-C8 criteria used for A-F, and state explicitly why it is rejected in favor of B (if it still is) — most plausibly because a tag/subject taxonomy still needs governance to avoid drift (which would then symmetrically apply the taxonomy-governance critique the document already levels at itself in IN-003 below), or because grep-by-filename is judged more valuable than grep-by-tag for the specific Jerry workflow. Either way, the comparison should be made explicit rather than left un-benchmarked.
**Acceptance Criteria:** The null-alternative section (or a new subsection) explicitly scores or reasons through the tag-registry-without-renaming option and states a definitive rejection rationale, not just an omission.

---

### IN-003-i4: Governance-burden objection against the null is applied asymmetrically to Scheme B's own design [MAJOR]

**Type:** Assumption stress test (A-1 adjacent; Internal Consistency)
**Original assumption:** "An index is itself governance — someone must build, run, and keep it fresh (a server-ish process the constraints reject, c-006)" (`:268`) is a valid reason the null alternative loses to B.
**Inversion:** Invert the objection and apply it to B's own design: does B's enforcement apparatus require an ongoing, humanly-maintained process of comparable or greater weight?
**Evidence:** Yes. The L2 Architectural Implications section names "Taxonomy governance is the new long-term liability... a soft process that can rot" and requires "a lightweight index (`docs/design/README.md`) and an arbiter" (`:406`). Migration item M-5b (`:499`) goes further: it requires **naming a human taxonomy arbiter "independent of `ps-architect`'s own compliance state,"** running an automated fuzzy-match against the repo-wide canonical-slug set, and having that arbiter "adjudicate flagged pairs on a per-ADR-creation cadence (checked at authoring time, not on an open-ended 'periodic' basis)." This is a heavier, more specific, more recurring human-process obligation than the "someone must build, run, and keep [an index] fresh" criticism leveled at the null alternative — B requires not just an index but a *named individual* performing *per-creation* adjudication, in addition to the index itself (M-5, `:498`).
**Plausibility:** High — this is drawn directly from the document's own text, not speculative.
**Consequence:** The null-alternative comparison is not internally consistent: it disqualifies the null for requiring an actively-maintained process while B's own accepted design requires a comparable or larger one (arbiter + fuzzy-match lint + index, versus just an index for the null). This does not necessarily flip the overall conclusion (B may still be justified on other grounds — citation stability chief among them, per IN-002's analysis), but the specific "an index is itself governance" argument, as stated, does not actually distinguish B from the null on the axis it claims to.
**Dimension:** Internal Consistency (0.20)
**Mitigation:** Either (a) drop or soften the "an index is itself governance" argument against the null (since B pays a comparable cost), and rest the null's rejection solely on the citation-stability argument (which is genuinely asymmetric in B's favor), or (b) explicitly acknowledge the symmetry and argue B's governance cost is justified by its additional citation-stability benefit relative to the null (a "we pay more governance, but get more benefit" framing, rather than "the null pays governance and we don't").
**Acceptance Criteria:** The "why it still loses to B" bullet list at `:268` is revised so the governance-burden argument is either removed or explicitly reconciled against M-5b's own arbiter requirement.

---

### IN-004-i4: `scope:` frontmatter field declared "mandatory" has no FAIL-class lint enforcement [MAJOR]

**Type:** Assumption (A-3)
**Original assumption:** "the `scope:` frontmatter field is **mandatory at authoring time**" (`ADR-PROJ031-004-adr-identifier-convention.md:291`; also `adr-standards-rule-draft.md:58`, ADR-M-013) "removes the dependence on authors classifying correctly" (`:291`-`292`).
**Inversion:** What if this "mandatory" declaration is never actually checked? Then an author who omits `scope:` faces zero consequence, and the field is optional in all but name.
**Evidence:** Scanning every lint rule in the L5 CI Lint Specification (`adr-standards-rule-draft.md:206-219`, mirrored at `ADR-PROJ031-004-adr-identifier-convention.md:647-660`): **no rule of any class (FAIL or WARN) checks for the mere presence of `scope:`.** L-5 ("Framework home," WARN) only checks that an ADR already marked `ACCEPTED` **and** `scope: framework` lives under `docs/design/` — it presupposes `scope:` is already set and says nothing if it is absent. L-6/L-6b check `origin_project`/`origin_entity`, not `scope`. No lint rule targets `scope:` presence for a newly-authored, `PROPOSED`, project-local ADR — which is precisely the population ADR-M-013 is written for ("Every new ADR SHOULD declare its intended `scope`... at authoring time").
**Plausibility:** High — directly verifiable by exhaustively reading the 12-row lint table, which contains no such rule.
**Consequence:** The Promotion-Frequency Sensitivity section's rebuttal to its own "authors know intent at birth" over-claim (`:291`) leans on `scope:` becoming a "mandatory declared field" as the mechanism that "removes the dependence on authors classifying correctly." Since no lint enforces its presence, the mechanism is prose-only, and the rebuttal's practical force is weaker than stated: an author under time pressure can skip `scope:` entirely with zero technical consequence, silently reintroducing exactly the dependence-on-correct-guessing the fix was designed to remove (the author now simply omits any declaration rather than declaring a wrong one — arguably a worse outcome, since even a wrong declaration is diagnosable, but a missing one is not).
**Dimension:** Internal Consistency (0.20); Methodological Rigor (0.20)
**Mitigation:** Add a FAIL- or at minimum WARN-class rule (e.g., L-6c) that checks `scope:` presence on any `PROPOSED`-or-`ACCEPTED` ADR under a canonical or dialect grammar, independent of the ADR's current status or eventual location.
**Acceptance Criteria:** The lint specification table includes a rule name checking `scope:` field presence, and ADR-M-013's "mandatory" language is either backed by that rule or downgraded to match its actual (advisory) enforcement level.

---

### IN-005-i4: Solo-maintainer waiver fallback reintroduces the self-certification weakness the audited-ledger redesign was built to eliminate [MAJOR]

**Type:** Assumption (A-1)
**Original assumption:** The audited waiver-ledger mechanism (structured entry, `>=40`-char justification, API-verified second-reviewer approval, `expires` date, append-only integrity checked by L-11) provides materially stronger rigor than the originally-rejected unaudited bare inline comment.
**Inversion:** What if, in the operating regime the document itself declares current, the "audited" mechanism collapses back to self-certification — i.e., the author of the violation is also its approver?
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:635-643` ("Solo-maintainer reality and waiver fallback, PM-102") discloses: `.github/CODEOWNERS` (verified 2026-07-02) "assigns **every** governed path... to the **single identity `@geekatron`**," so "a 'distinct GitHub identity with review authority' **does not exist today**," making "FAIL-rule waivers... **non-exercisable** in practice until a second maintainer/reviewer exists" (`:637`). The disclosed fallback (`:642`) then permits **that same sole maintainer to approve their own waiver**, gated only by (a) the standard ledger fields, (b) a `solo_maintainer: true` flag, and (c) a `review_by` date. Critically, the >=40-character "justification" field has no independent reviewer to reject it — it is checked only for length/presence, not for merit, once the solo flag is set.
**Plausibility:** High. This is the document's own designed mechanism, not a hypothetical; and CODEOWNERS is verified single-identity by the document itself.
**Consequence:** Under the current and (per the document's own framing, `:643` "onboarding a second reviewer are organizational actions... outside this document's edit mandate") likely near-term-persistent operating regime, **every FAIL-class rule (L-1 through L-12) is waivable by the same person whose commit triggered the FAIL, with a self-written justification and no independent check.** This is functionally the same governance strength as the originally-rejected design the document explicitly calls out as inadequate: "The pre-review draft let a bare, unreviewed `adr-lint: ignore` comment bypass a FAIL rule — self-contradicting 'FAIL rules block CI'" (`:627`). The solo-maintainer fallback substitutes a structured YAML entry and a boolean flag for the bare comment, which improves *auditability/visibility* (a real, disclosed benefit — the document is honest that this is "visible and auditable... not disguised," `:642`) but does **not** restore *independent review*, which was the actual property the RT-004 redesign was meant to add. The elaborate API-verified-approver design (L-11, CODEOWNERS cross-check) is therefore inert for the repo's actual current governance topology, and the document's Enforcement Design section reads as though independent review is the norm when, by its own admission, it currently is not.
**Dimension:** Methodological Rigor (0.20); Internal Consistency (0.20)
**Mitigation:** State explicitly, in the Enforcement Design summary (not only in the buried PM-102 subsection), that **until a second CODEOWNER exists, every FAIL-class lint rule is de facto self-waivable** — i.e., advisory in effect, not merely "advisory until M-6 ships" as currently framed. This is a materially different and stronger caveat than "the lint doesn't exist yet"; it says that even after the lint exists, its override path is currently equivalent in rigor to an unaudited comment. Consider whether a stronger interim control is feasible (e.g., a mandatory cool-down period before a solo-approved waiver takes effect, or a hard cap on the number of solo-approved waivers active at once) rather than relying solely on visibility.
**Acceptance Criteria:** The Enforcement Design summary and/or Status section explicitly states the solo-maintainer waiver equivalence to unaudited override, so a reader evaluating "is this convention really enforced" is not misled by the elaborate audited-ledger prose into believing independent review currently occurs.

---

### IN-006-i4: `canonical_id` field used in this ADR's own frontmatter is absent from the Frontmatter Schema the convention itself defines [MAJOR]

**Type:** Anti-Goal / Internal Consistency (self-compliance)
**Original assumption (A-5):** The Frontmatter Schema as published is complete and matches what a compliant ADR (including this one) actually needs to carry.
**Inversion:** Invert the self-compliance claim: does this ADR's own frontmatter use any field the schema it defines does not recognize?
**Evidence:** This ADR's own YAML frontmatter block (`ADR-PROJ031-004-adr-identifier-convention.md:1-16`) includes `canonical_id: ADR-adr-convention-001` (`:15`), explicitly commented as "declared remap target (non-schema advisory field; see Meta-Note)" and reiterated at `:18` ("`canonical_id` ... (non-schema advisory field; see Meta-Note)"). However, the canonical **Frontmatter Schema** published by this same ADR (`:339-355`, "L1: Technical Implementation") lists exactly `id, type, status, scope, origin_project, origin_entity, created, supersedes, superseded_by, amends, amended_by, promoted_from, promoted_to` — **no `canonical_id` field.** The companion rule draft's own Frontmatter Schema (`adr-standards-rule-draft.md:114-129`) likewise omits it. The field is used, admits itself to be non-standard, and is never added to the schema as even an OPTIONAL field for other dialect-ADR authors in the same "written under the discouraged dialect but destined for Path-2 promotion" situation this ADR itself is in.
**Plausibility:** High — directly verifiable from the frontmatter text and the schema definition, both quoted above.
**Consequence:** Any *other* dialect ADR author who, like this ADR's author, wants to declare "I know my eventual canonical ID already, even though my current filename is the discouraged dialect" has no standardized field to do so — they would have to invent their own `canonical_id`-equivalent, non-schema field, exactly reproducing this gap. The convention thereby fails to generalize a mechanism it demonstrably found useful enough to use on itself, undermining the "worked example of its own Path-2 promotion rules" framing (`:689`) — the worked example uses a mechanism the rules don't actually offer to anyone else.
**Dimension:** Internal Consistency (0.20); Completeness (0.20)
**Mitigation:** Add `canonical_id` (optional, null-by-default) to the published Frontmatter Schema in both documents, documented as "the declared eventual canonical identity for a dialect ADR whose author already knows its Path-2 destination — advisory only, has no lint enforcement, purely informational until promotion actually occurs."
**Acceptance Criteria:** `canonical_id` appears in both Frontmatter Schema code blocks as a documented (even if optional/advisory) field, OR this ADR's own use of it is removed/replaced with an in-scope mechanism (e.g., a prose note rather than a frontmatter field) so the schema and the ADR's own practice are consistent.

---

### IN-007-i4: Cross-iteration score trend does not support the "patch-in-place converges" assumption [MAJOR]

**Type:** Assumption (A-6)
**Original assumption:** The remediation strategy used across iterations 1-4 (respond to each adversarial round by adding corrections, disclosures, and caveats to the existing document) is converging toward the 0.95 engagement gate.
**Inversion:** What would falsify convergence? A score trend that goes down, or that only partially recovers, across successive full remediation cycles.
**Evidence:** The ADR's own Changelog reports, verbatim: v1.1 "after adversarial iteration 1 (score 0.67 → re-review; engagement gate 0.95)" (`:743`); v1.2 "after adversarial iteration 2 (score 0.54; engagement gate 0.95)" (`:744`); v1.3 "after adversarial iteration 3 (score 0.62; engagement gate 0.95; weakest dim Internal Consistency 0.55)" (`:745`); v1.4 "Owner S-010 self-refine after adversarial iteration 4 (Group A)" — a narrower pass addressing four specific self-refine items (SM-201..204), not a full-tournament remediation (`:746`). The trajectory 0.67 → 0.54 → 0.62 is **not monotonically improving** across three full remediation cycles, and remains roughly 0.30-0.41 short of the 0.95 gate after three complete rounds.
**Plausibility:** High — this is the document's own self-reported data, not an external estimate.
**Consequence:** A document that both grows in length/density with each cycle (new disclosure blocks, correction notes, and cross-references to prior review tags accumulate rather than get pruned — evident from the sheer density of parenthetical `(FM-NNN, iter-N)`-style annotations throughout) and shows a non-monotonic, still-distant score trend raises the possibility that the remediation strategy itself (respond-and-annotate-in-place) is treating symptoms (specific point findings) rather than the root structural cause (the document's own escalating complexity may itself be *creating* new findings faster than existing ones are resolved — an accretion dynamic). This is stated as inference, not fact: three iterations is a small sample, and iteration 2's dip to 0.54 could reflect a stricter or differently-focused reviewer rather than genuine regression.
**Dimension:** Internal Consistency (0.20); Completeness (0.20)
**Mitigation:** Before iteration 5, consider a structural pass (not just point-fixes): identify whether specific sections could be extracted, shortened, or moved to a separate reference document (e.g., the extensive prior-iteration meta-commentary, which the document's own "Reading note" at `:65` already tells readers "carries no normative force" and can be safely ignored) to reduce the surface area a fresh reviewer must re-verify, rather than continuing to add net-new prose on top of already-dense text.
**Acceptance Criteria:** Iteration 5's remediation notes explicitly address whether document length/density itself is a contributing factor to score variance, and/or a structural simplification is attempted and its effect on score is measured.

---

### IN-008-i4: Recurring corpus-count corrections across iterations undermine confidence in figures the unbuilt regression test will depend on [MAJOR]

**Type:** Assumption (A-7)
**Original assumption:** Manual, per-iteration filesystem verification of the grandfathered ADR corpus has now converged on stable, correct counts.
**Inversion:** What if the counting methodology itself is unreliable, such that the count could change again in iteration 5, and the (not-yet-built) L-1 regression test's "16-file" fixture is therefore unverified against a moving target?
**Evidence:** The document itself discloses at least three distinct count corrections across its four iterations: (1) D-4's own "Count reconciliation (SM-201, iter-4)" (`:226`) explicitly reconciles an earlier "~11" figure (project-ID-scoped subfamily) against the current "16" (whole dialect corpus), stating these "count different sets, not the same set inconsistently" — itself an admission that a naive reader (or a script author building the regression-test fixture) could easily conflate the two; (2) the EPIC-002 promotion-count correction (`:287`, "the cited advocate source... reports '1 of EPIC-002's **2** ADRs'; this ADR reports **1-of-3**"); (3) the M-14 count reconciliation (`:508`, "SM-102 count reconciliation: 14 = the 15 pre-existing dialect ADRs minus the one entity-embedded `STORY015` ADR"); (4) the ps-architect.md occurrence-count dispute across iterations, ultimately resolved into a line-by-line breakdown rather than a single scalar (`:506`, "Neither the earlier '~6' nor the finding's '10' was a complete scalar"). The Migration Plan's own gating regression test (`:625-626`) commits to "15 uppercase entity-dialect files... **plus** the GH-issue singleton... **plus** the 3 `docs/design/` canonical ADRs" as "19 files exercised in total," while the narrative elsewhere states "16" as the live dialect-set total (`:226`, `:503-504`) — two different totals (16 vs. 19) appear to describe overlapping-but-differently-scoped corpora (16 = dialect-only; 19 = dialect + 3 canonical framework ADRs), which is plausible but is not explicitly reconciled at the point both numbers appear.
**Plausibility:** High — every count cited above is drawn verbatim from the document's own text, which repeatedly self-corrects.
**Consequence:** The L-1 regression test (M-6 gating criterion, `:625-626`) is described as validating against these manually-derived counts, but since the count has changed at least three times across four iterations of the *same* author re-verifying the *same* live corpus, there is a real risk the eventual test fixture is built against a count that will need a fourth correction once the lint is actually implemented and run against the true corpus — at which point the "16-file... green" ratification criterion (G-2, `:92`) could itself require yet another revision cycle.
**Dimension:** Evidence Quality (0.15); Methodological Rigor (0.20)
**Mitigation:** Before or as part of M-6, generate the regression-test fixture list via an actual filesystem query (e.g., a `find`/`glob` command run and its raw output pasted into the document) rather than continuing manual narrative counting; this converts a fact repeatedly re-derived by hand into a single, reproducible, script-verifiable artifact.
**Acceptance Criteria:** The 16-file (or 19-file) regression corpus is backed by a literal command-and-output pair in the document (as is already done for the pre-flight collision-check one-liner at `:388-397`), not by narrative enumeration alone.

---

### IN-009-i4: Title-slug preservation during promotion is guidance-only, with no corresponding lint rule [MINOR]

**Type:** Assumption (A-8)
**Original assumption:** Prose guidance is sufficient to prevent title-slug re-slugging during a Path-1 promotion `git mv`.
**Inversion:** What if an author re-slugs the title tail during promotion anyway, since nothing technically prevents it?
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:528` states the title-slug tail "SHOULD be preserved unchanged during the move too (DA-006, iter-3)... re-slugging the title tail during a promotion is a needless second churn source and is discouraged." No lint rule among L-1 through L-12 checks whether a promoted file's title-slug tail matches its pre-promotion tail.
**Plausibility:** Medium — a low-cost, easily-overlooked slip during a manual `git mv`, not a structural failure mode.
**Consequence:** Minor residual full-path-citation churn risk during promotions, symmetrical to the already-disclosed ~28% full-path-citation caveat (`:530`) but specifically for the title-slug component, which the Path-1 "zero churn" framing does not fully account for if title-slugs drift in practice.
**Dimension:** Actionability (0.15)
**Mitigation:** Add a lightweight WARN-class lint check comparing the title-slug substring before/after a detected promotion (e.g., via git history diff of `decisions/` moves), or simply accept this as a documented, low-severity residual alongside the existing full-path-citation caveat.
**Acceptance Criteria:** Either a WARN rule is added, or this residual is explicitly folded into the existing Path 1 full-path-citation caveat as a named sub-case.

---

## Zero-Governance Null-Alternative Re-Benchmark

The invoking task explicitly asked: *if we wanted maximum decision-findability with zero governance, what would we do — and does the package beat that null alternative?* This re-runs that comparison independently of the deliverable's own IN-004 (iter-2/3-tagged) null-alternative section, per the Inversion protocol's Step 2 (goal inversion).

**Strongest true-zero-governance design:** Rename nothing, add no rule, rely entirely on `grep`/full-text/semantic search across existing filenames and prose. **Verdict: package (Scheme B) clearly beats this.** The document's own argument holds: search does not fix a broken hyperlink/path reference, and citation-integrity (not discoverability) is the load-bearing, demonstrated failure (`:266-267`). Confirmed independently in this execution — no counter-evidence found.

**Strongest low-(not-zero)-governance design (the gap identified as IN-002):** Freeze every existing filename permanently (zero renames, ever — including for the 16 currently-grandfathered dialect ADRs and any future ADR), and add only a frontmatter `tags:`/`subject:` field plus a generated (not hand-maintained) registry file, with no ID-grammar lint at all. **Verdict against this stronger competitor: the package's advantage narrows but does not fully close.** Package (B) still wins on:
- **Filename-level discoverability** (`grep -r "ADR-agent-" docs/design/` works without opening a registry file; the tag alternative requires consulting the generated index first) — a real, if secondary, ergonomic advantage.
- **Simplicity of the "what is this file about" signal** for anyone browsing the filesystem directly (e.g., in a file explorer, not just via search tooling).

The tag alternative matches or beats B on:
- **Citation stability** — strictly better, since literally nothing is ever renamed under the tag alternative (not even the discouraged-dialect ADRs), whereas B still has a live, if now-discouraged, Path-2 rename case.
- **Governance cost** — lower, since no 12-rule filename-grammar lint, no L-1/L-2/L-3/L-4/L-9 filename-family policing, and no waiver-ledger machinery tied to filename correctness is needed at all (only a much smaller tag-drift concern remains, symmetrical to B's own taxonomy-arbiter burden per IN-003).

**Overall verdict:** The package is well-justified against the true-zero-governance null, but the requested inversion surfaces that the *documented* benchmark (`:263-269`) tests against the weaker of the two plausible low-governance alternatives. Restated honestly: **the package beats "do nothing," but the document does not demonstrate it beats "do almost nothing" (tag-only, zero-rename).** This does not mean Scheme B is the wrong choice — its citation-stability argument versus true zero-governance is sound, and its filename-level discoverability edge over the tag alternative is real — but the comparison as published overstates how decisively the package wins against the full space of low-governance alternatives, because it never named or scored the stronger competitor. See IN-002-i4 and IN-003-i4 for the corresponding structural findings.

---

## Recommendations

**Critical (MUST mitigate before ratification proceeds):**
- **IN-001-i4** — Decouple ratification into a guidance tier (immediate) and an enforcement tier (non-blocking milestone), or explicitly justify why all-or-nothing bundling is acceptable given the document's own R-5/FM-1 risk disclosures.

**Major (SHOULD mitigate):**
- **IN-002-i4** — Add and score the tag-registry-without-renaming alternative explicitly in the null-alternative section.
- **IN-003-i4** — Reconcile or remove the "an index is itself governance" argument given M-5b's comparable arbiter burden.
- **IN-004-i4** — Add a lint rule (FAIL or WARN) checking `scope:` presence, or downgrade "mandatory" language to match actual (zero) enforcement.
- **IN-005-i4** — State plainly in the Enforcement Design summary that FAIL rules are currently self-waivable under the single-CODEOWNERS reality, not merely "advisory until M-6."
- **IN-006-i4** — Add `canonical_id` to the published Frontmatter Schema (or remove its use), so the ADR's own frontmatter is schema-compliant.
- **IN-007-i4** — Consider a structural (not only point-fix) pass before iteration 5, given the non-monotonic 0.67→0.54→0.62 score trend.
- **IN-008-i4** — Back the regression-test corpus count with a literal reproducible command output, not narrative enumeration, given the repeated manual recount corrections.

**Minor (MAY mitigate):**
- **IN-009-i4** — Add a WARN check for title-slug drift during promotion, or fold it into the existing full-path-citation caveat.

---

## Scoring Impact

Mapping this execution's findings to the S-014 dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10):

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-002-i4: null-alternative benchmark omits a credible middle option; IN-006-i4: Frontmatter Schema omits a field the ADR itself uses; IN-007-i4: goal inventory never explicitly names/tests "ratify + adopt" and "converge to 0.95" as goals in their own right |
| Internal Consistency | 0.20 | Negative | IN-003-i4: governance-burden objection applied asymmetrically; IN-004-i4: "mandatory" prose contradicted by zero lint enforcement; IN-005-i4: audited-waiver framing contradicted by disclosed solo-self-approval reality; IN-006-i4: ADR's own frontmatter violates its own published schema |
| Methodological Rigor | 0.20 | Negative | IN-001-i4: ratification-gate design conflates guidance-adoption with tooling build-out; IN-005-i4: override mechanism collapses to self-certification in the documented operating regime; IN-008-i4: regression-test fixture rests on repeatedly-corrected manual counts rather than a reproducible query |
| Evidence Quality | 0.15 | Mixed | Positive: every finding in this report traces to specific, quoted, line-cited text in the deliverable itself, and several (IN-005, IN-007, IN-008) use the deliverable's own self-disclosed data (verified CODEOWNERS state, Changelog scores, recount corrections) as evidence, strengthening rather than merely asserting the findings. Negative: IN-008-i4 identifies that the deliverable's OWN evidence base (corpus counts) has been unstable across iterations. |
| Actionability | 0.15 | Negative | IN-001-i4: no two-tier ratification path currently exists to act on; IN-004-i4 and IN-009-i4 each identify a "SHOULD"/"mandatory" claim with no corresponding checkable mechanism |
| Traceability | 0.10 | Neutral-to-Positive | The deliverable's extensive cross-referencing (prior-review tags, line-pinned citations) makes independent verification of every finding in this report straightforward; this report itself follows the same discipline (IN-NNN-i4 identifiers, line-cited evidence throughout) |

---

## Execution Statistics

- **Total Findings:** 9
- **Critical:** 1 (IN-001-i4)
- **Major:** 7 (IN-002-i4 through IN-008-i4)
- **Minor:** 1 (IN-009-i4)
- **Goals Stated/Inverted:** 7 (5 explicit, 2 implicit)
- **Assumptions Mapped:** 8
- **Vulnerable Assumptions (Major+):** 7
- **Protocol Steps Completed:** 6 of 6 (Goals stated; Anti-goals inverted; Assumptions mapped; Assumptions stress-tested; Mitigations developed; Synthesis/scoring completed)

---

*Report generated by adv-executor per S-013 (Inversion Technique), iteration 4, blind-protocol tournament review. No files outside this output path were modified. No prior-iteration adversary findings were consulted (blind protocol compliance).*
