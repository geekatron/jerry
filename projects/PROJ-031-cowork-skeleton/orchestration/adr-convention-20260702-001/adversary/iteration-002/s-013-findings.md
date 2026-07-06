# Inversion Report: ADR-PROJ031-004 (ADR Identifier, Location, and Promotion Convention) + Companion Rule Draft

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement quality gate 0.95)
**Date:** 2026-07-02
**Reviewer:** adv-executor (blind, independent — iteration 2)
**H-16 Compliance:** S-003 Steelman confirmed applied in substance — the deliverable itself embeds a "Strongest case (steelman, from `advocate-*.md`)" subsection for every one of Options A-F and cites H-16 explicitly (ADR lines 115, 447). Per BLIND PROTOCOL, the iteration-1 S-003 execution report itself was not read (adversary/ directory off-limits to this reviewer).
**Goals Analyzed:** 7 | **Assumptions Mapped:** 6 (explicit + implicit) | **Vulnerable Assumptions:** 6 (1 Critical, 4 Major, 1 Minor+informational cluster)

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Step 1-2: Goals and Anti-Goals](#step-1-2-goals-and-anti-goals) | Stated goals, inverted anti-goals, guaranteed-failure checklist |
| [Step 3-4: Assumption Map and Stress Tests](#step-3-4-assumption-map-and-stress-tests) | Assumption inventory with stress-test results |
| [Findings Table](#findings-table) | All findings, severity-classified |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Zero-Governance Null Alternative (Explicit Inversion)](#zero-governance-null-alternative-explicit-inversion) | Response to the task's explicit inverted-goal benchmark |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Finding counts |

---

## Summary

The deliverable is unusually rigorous — it already performs partial self-inversion (its own "Inversion check (S-013)" note at ADR line 399) and survived one adversarial remediation round (v1.0 → v1.1). Applying the full S-013 methodology externally still surfaces **one Critical and four Major vulnerabilities**, the most significant being a direct internal contradiction between evidence the ADR itself cites (GOV.UK's maturity-gradient principle: framework-scope is not knowable at birth) and the premise its own core mitigation (D-3's "authors know intent at birth") depends on — a premise contradicted by the document's own 3-for-3 historical rename record. Recommendation: **REVISE** before ratification (M-1) — the Critical finding (IN-001) touches the ADR's central value proposition (citation-stable promotion) and should be resolved or explicitly risk-accepted with a named owner, not silently carried forward.

---

## Step 1-2: Goals and Anti-Goals

### Stated/inferred goals (Step 1)

| # | Goal | Source |
|---|------|--------|
| G1 | Promotion of an ADR from project → framework MUST NOT break citations (default = pure file move) | ADR L0, Decision D-2 |
| G2 | Prevent ID collisions across many concurrent, uncoordinated branches, with no central registry/server process | Constraint c-006 |
| G3 | Preserve provenance (origin) losslessly, moved from identity to frontmatter | Constraint c-005, D-1 |
| G4 | No big-bang renumbering of the legacy corpus; adopt-forward only | Constraint c-003, D-4 |
| G5 | Convention stays MEDIUM-tier (not HARD) yet is *actually* enforced, not merely advisory | Constraint c-001/c-002, D-5, R-5 |
| G6 | Net improvement in decision-findability/discoverability vs. today's zoo of ID families | Force 4, Consequences #2 |
| G7 | The ADR is a genuine self-compliance worked example (own Path-2 self-promotion, M-9) | Meta-Note, Changelog v1.1 |

### Anti-goals: "what would GUARANTEE this convention fails or makes the repo worse?" (Step 2)

| # | Guaranteed-failure condition | Does the package do this? |
|---|---|---|
| AG-1 | Mass-renumber/rename the existing corpus on adoption | **Avoided** — D-4 grandfathers 16 legacy dialect files in place |
| AG-2 | Add a new HARD rule while the ceiling sits at 25/25 | **Avoided** — explicit MEDIUM tier (c-001) |
| AG-3 | Ship a FAIL-class lint that rejects the very corpus it promises to preserve | **Avoided in this iteration** — the L-1a/L-1b split + mandatory 16-file regression test is the documented fix for exactly this iteration-1 defect |
| AG-4 | Require a central registry/server process in a monorepo with many concurrent branches | **Avoided** — `sort \| uniq -d`, no server (c-006) |
| AG-5 | Let promotion keep breaking citations for the framework-bound ADRs that matter most | **AT RISK** — see [IN-001](#in-001-d-3s-at-birth-classification-premise-is-contradicted-by-the-documents-own-cited-evidence-critical) |
| AG-6 | Let semantic (near-duplicate) taxonomy collisions go structurally undetected | **AT RISK** — see [IN-002](#in-002-asymmetric-collision-enforcement-structural-vs-semantic-major) |
| AG-7 | Let the flagship governance document itself violate the rule it establishes, once live | **AT RISK** — see [IN-003](#in-003-l-8-has-no-exemption-for-live-documents-that-cite-stale-ids-as-evidence-major) |
| AG-8 | Let the "self-compliance" demonstration (M-9) be talked about but never actually gated to completion | **AT RISK** — see [IN-004](#in-004-gating-semantics-contradiction-ratification-precondition-vs-m-9s-on-acceptance-annotation-major) |
| AG-9 | Adopt more governance than doing nothing would have achieved | **Unproven, not disproven** — see [IN-005](#in-005-the-null-alternative-rebuts-a-weak-null-not-the-strongest-available-one-major) |

Four of nine guaranteed-failure conditions are cleanly avoided (AG-1 through AG-4) — this is genuine, verifiable strength, not just self-assessment. Five (AG-5 through AG-9) are live, evidence-grounded risks addressed below.

---

## Step 3-4: Assumption Map and Stress Tests

| Assum. ID | Assumption (explicit/implicit) | Category | Confidence | Stress-test result |
|---|---|---|---|---|
| A1 | "Promotion of project decisions into the framework is a first-class, recurring operation" | Explicit (Status section) | Medium (ADR's own stated 0.78) | Already rigorously stress-tested by the ADR's own Promotion-Frequency Sensitivity section (tipping point, bimodal refinement, adverse-regime disclosure). Well-handled; residual risk explicitly owned. No new finding beyond what the document already discloses. |
| A2 | Domain-slug taxonomy will not need centrally-enforced governance beyond a WARN-level fuzzy-match suggestion (M-5b) | Implicit (Process) | Low-Medium | **FAILS** — see IN-002 (Major) |
| A3 | Authors can/will correctly self-classify framework-vs-project scope at ADR-authoring time (the premise D-3's "SHOULD prefer domain slug from birth" safety valve depends on) | Implicit (Process/Temporal) | Low (contradicted by the document's own cited source) | **FAILS** — see IN-001 (Critical) |
| A4 | No central registry/index is desirable or necessary; `sort \| uniq -d` + file-move is the correct zero-governance mechanism | Explicit (c-006) | High for the "no server process" half; unverified for the "no index would help" half | **Partially fails on the null-alternative dimension** — see IN-005 (Major) |
| A5 | The waiver ledger's `approved_by` field meaningfully prevents self-approval of FAIL-rule overrides | Implicit (Process) | Low | **FAILS (minor)** — see IN-006 (Minor) |
| A6 | L-8's repo-wide free-text citation scan will only ever encounter genuinely broken citations, never legitimate evidentiary citations to known-stale IDs | Implicit (Technical/Evidence) | Low | **FAILS** — see IN-003 (Major) |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260702iter2 | A3: authors self-classify framework-scope at birth | Assumption | Low | **Critical** | ADR L48, L127, L135, L251 (self-contradiction, see below) | Internal Consistency, Methodological Rigor |
| IN-002-20260702iter2 | A2: taxonomy sprawl covered by soft process only | Assumption | Low-Medium | **Major** | ADR L346, L379-382, L397; rule draft L47, L55, L185-203 (no L-1..L-8 rule covers synonymy) | Completeness, Methodological Rigor |
| IN-003-20260702iter2 | A6: L-8 citation scan has no evidentiary-citation exemption | Assumption | Low | **Major** | rule draft L197, L201; ADR L64, L595 (this doc's own stale-ID citations) | Evidence Quality, Internal Consistency |
| IN-004-20260702iter2 | Anti-Goal: M-9 self-compliance demonstration ungated relative to M-6 | Anti-Goal | N/A | **Major** | ADR L420, L434 vs. L431 (gating-language inconsistency) | Internal Consistency, Actionability |
| IN-005-20260702iter2 | A4: strongest null alternative not tested | Assumption | Low-Medium | **Major** | ADR L225-231; `explore/trade-study.md` (Options A-F, no hash/ULID/generated-index option); no hits for hash/ULID in explore/ or research doc | Completeness, Methodological Rigor |
| IN-006-20260702iter2 | A5: waiver `approved_by` is a bare string check | Assumption | Low | Minor | rule draft L185 | Actionability |
| IN-007-20260702iter2 | Anti-Goal: pre-flight collision command not wired as a hook | Anti-Goal | N/A | Minor | ADR L326-337 | Actionability |
| IN-008-20260702iter2 | Anti-Goal: embedded self-"Inversion check" mistaken for full S-013 execution | Anti-Goal | N/A | Minor (informational) | ADR L399 (one paragraph, no assumption map, no IN-NNN IDs) | Traceability |

**Finding ID format used:** `IN-{NNN}-20260702iter2` (execution_id = `20260702iter2`), per template Output Format §3.

---

## Finding Details

### IN-001: D-3's at-birth-classification premise is contradicted by the document's own cited evidence [CRITICAL]

**Type:** Assumption
**Original Assumption:** D-3's safety valve — the mechanism meant to keep Path 1 (zero-churn promotion) the common case — rests on the claim that "the author usually knows the intent at birth" (ADR L251: "framework-relevance is a knowable, declarable property at authoring time, not a retroactive guess").
**Inversion:** Assume the opposite — authors generally do *not* know at authoring time whether a decision will become framework-governing.
**Plausibility:** High. The same document, in its own Scheme-C steelman (L135), approvingly cites GOV.UK's maturity-gradient principle: *"you typically do not know an ADR is framework-wide the day you write it; you learn it by living with it inside a project first"* (`adr-convention-standards-research.md:110-112`). Separately, the document's own historical record (L48, L127) states that **all three** existing framework ADRs were born under the old origin-encoded scheme and were *force-renamed* on promotion (`commit 41539073`) — i.e., 3-for-3, the authors did **not** pick a durable, subject-encoded identity at birth. These two facts — cited approvingly in the same document — directly contradict the L251 claim that framework-relevance is knowable and declarable at birth.
**Confidence:** Low (that the L251 premise holds) / High (that the contradiction exists in the text as written).
**Consequence:** D-3 is the mechanism intended to make Path 1 (the ADR's central selling point — zero-citation-churn promotion) the norm rather than the exception for framework-bound decisions. If at-birth classification is generally unreliable — as the document's own cited authority and its own historical sample both indicate — then D-3's "SHOULD prefer a domain slug from birth" guidance will not reliably fire for the population that matters most (future framework ADRs), Path 2 (the discouraged rename+tombstone path) becomes the effective default for exactly those decisions, and the citation-break failure mode the ADR exists to eliminate (still-unrepaired `ADR-PROJ007-001/002` citations, per the ADR's own admission at L48/L249) recurs. This is not a residual edge case; it is the expected outcome for the highest-value population under the document's own logic.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:48` ("all three framework ADRs were born inside projects and renamed on promotion... the resulting broken citations remain unrepaired"); `:127` ("all three framework ADRs were born under A/C identity and force-migrated to domain-slug... a paid promotion tax with a git receipt"); `:135` (GOV.UK maturity-gradient citation, approvingly used to steelman Scheme C); `:251` ("the author usually knows the intent at birth... a knowable, declarable property at authoring time, not a retroactive guess," citing `advocate-domain-slug.md:133`).
**Dimension:** Internal Consistency (primary); Methodological Rigor (secondary — the existing FM-3 risk entry treats this as an "authors overused the dialect" *discipline* problem rather than the *structural foresight-limitation* problem the document's own GOV.UK citation implies, so the risk's stated occurrence (MED, ADR L396) and its "SHOULD-guidance" mitigation likely understate/undertreat it).
**Mitigation:** Either (a) reconcile the contradiction explicitly — concede that at-birth classification is unreliable and strengthen D-3 from a SHOULD-guidance to a required declaration step at ADR-creation time (e.g., a mandatory `intended_scope: local | framework | unsure` frontmatter field with `unsure` defaulting to domain-slug, removing the silent-failure path), or (b) explicitly accept the residual risk with a named owner and a monitoring metric (e.g., track the Path-2 rename rate over the next N promotions and revisit if it does not trend toward zero).
**Acceptance Criteria:** The ADR's Rationale/Sensitivity section explicitly addresses the GOV.UK-vs-L251 tension (rather than citing GOV.UK approvingly in one place and contradicting it in another), and either D-3 is strengthened or the residual Path-2 recurrence risk is named as an owned, monitored risk distinct from FM-3's current "abuse" framing.

---

### IN-002: Asymmetric collision enforcement — structural vs. semantic [MAJOR]

**Type:** Assumption
**Original Assumption:** The L5 lint suite (L-1 through L-8) provides adequate collision protection for the convention's chosen identity scheme.
**Inversion:** Assume that exact-string collisions are rare in practice but near-duplicate (synonymous) slug collisions are common — the reverse of what the enforcement design assumes.
**Plausibility:** Medium-High. The ADR itself rates this scenario's occurrence as **MED-HIGH** (FM-4, L397: "The taxonomy sprawled (`agent-design`/`agent-definition`/`agents`); clustering broke; discoverability — the main win — degraded") and separately names taxonomy governance as "the new long-term liability" (L346).
**Consequence:** Despite this self-assessed MED-HIGH likelihood, none of the eight lint rules (L-1a/b, L-2 through L-8; rule draft L189-197, ADR L530-540) checks for near-duplicate/synonymous domain slugs. The only mitigation is M-5b (rule draft L47/ADR L430): a **SHOULD**-level behavior for the `ps-architect` agent to *manually* run a fuzzy-match check "at ADR-creation time" — not a CI gate, not wired into L-1 through L-8, and inapplicable if a human or a different agent authors the ADR file directly. Structural (exact) ID collisions get a non-waivable FAIL rule (L-3); the self-assessed *more likely* semantic-collision failure mode gets no deterministic check at all. This is a rigor asymmetry: the deliverable's stated core value ("deterministic, zero-token... enforcement," ADR L523) does not extend to the risk it itself rates highest among taxonomy failures.
**Evidence:** ADR `:346` ("Taxonomy governance is the new long-term liability"), `:379-382` (R-3), `:397` (FM-4, Occurrence MED-HIGH); rule draft `:47` (ADR-M-003), `:55` (ADR-M-011), `:185-203` (L5 Lint Specification — no synonymy rule present).
**Dimension:** Completeness (the enforcement design omits its own highest-rated risk category); Methodological Rigor.
**Mitigation:** Promote the fuzzy-match check from an agent-behavior suggestion (M-5b) to a deterministic WARN-class lint rule (e.g., `L-9 Taxonomy synonymy`, computing a Levenshtein/token-overlap distance between every new slug and the `docs/design/README.md` registry, WARN if below a threshold) so the check fires regardless of which agent or human authors the file.
**Acceptance Criteria:** A new lint rule (or an explicit, disclosed decision not to add one, with rationale) appears in the L5 Lint Specification table addressing near-duplicate slug detection, closing the gap between FM-4's self-rated MED-HIGH occurrence and its current zero-CI-coverage mitigation.

---

### IN-003: L-8 has no exemption for live documents that cite stale IDs as evidence [MAJOR]

**Type:** Assumption
**Original Assumption:** L-8's repo-wide free-text citation scan ("every referenced ID must resolve to a live ADR file at its cited path," rule draft L197) will only ever encounter citations that are meant to function as live links.
**Inversion:** Assume instead that a live governance document deliberately cites a *known-broken* ID as illustrative evidence (not as a functioning link) — does L-8 handle this correctly?
**Plausibility:** High — it is not hypothetical. **This very deliverable does it.** ADR-PROJ031-004 itself cites `ADR-CI-001` (confirmed dangling — the cited path `projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md` does not exist in the repo, verified via Glob) and `ADR-PROJ007-001/002` (confirmed still-stale per the ADR's own admission) repeatedly, by design, as evidence that citation breakage occurs. L-8's only stated exemption is for "append-only historical records (CHANGELOGs, `git` commit messages, release notes)" (rule draft L201; ADR L525-528). A live `decisions/`/`docs/design/` ADR that quotes a stale ID as *evidence in its own Context/References section* is neither a CHANGELOG nor a commit message, so it falls outside the stated exemption.
**Consequence:** Once this ADR is promoted (M-9, Path 2) into `docs/design/`, or even left in place at `projects/PROJ-031-cowork-skeleton/decisions/`, its own L-8 WARN check would likely flag its own References/Context sections — a false-positive against the flagship self-compliance document, undermining confidence in the lint's precision exactly where it matters most (the document meant to model correct behavior). Because L-8 is WARN (not FAIL), this does not block CI, but it does generate persistent noise that could train reviewers to ignore L-8 warnings generally (alert fatigue), weakening the lint's practical value over time.
**Evidence:** `.github/workflows/ci.yml:2` (verified dangling: `# ADR: projects/PROJ-001-plugin-cleanup/decisions/ADR-CI-001-cicd-pipeline.md` — path confirmed non-existent via Glob); ADR `:64` (still-stale PROJ-007 citation acknowledgment), `:595` (References table repeating the same stale IDs as evidence); rule draft `:197`, `:201` (L-8 spec and exemption list, no "cited-as-evidence" carve-out).
**Dimension:** Evidence Quality (the lint's own precision is compromised on the document that most needs to model correctness); Internal Consistency.
**Mitigation:** Add an explicit L-8 exemption for citations that are visibly evidentiary rather than functional — e.g., citations inside a fenced code block, inside a `References`/`P-022 disclosures` table cell explicitly marked as historical evidence, or preceded by a documented inline marker (`<!-- stale-citation-example -->`). Alternatively, scope L-8 to specific link syntaxes (markdown links, `link-artifact` calls) rather than any bare `ADR-[A-Za-z0-9-]+-\d{3}` token in prose.
**Acceptance Criteria:** The L-8 spec documents how a live governance document may cite a known-stale ID as evidence without generating a lint warning, and a dry-run of L-8 against this ADR's own text (once implemented) produces zero false positives.

---

### IN-004: Gating-semantics contradiction — ratification precondition vs. M-9's "on acceptance" annotation [MAJOR]

**Type:** Anti-Goal
**Original claim:** "Ratification (`PROPOSED` → `ACCEPTED`) is conditional on independently-verified completion of every gating item, M-6 in particular" (ADR L420).
**Inversion:** Assume "every gating item" is read literally — then M-9 (marked "Yes (on acceptance)," ADR L434) must *also* complete before the status can flip to `ACCEPTED`. But Path-2 self-promotion (M-9's own content) presumes an already-`ACCEPTED` ADR is being promoted/tombstoned — the mechanic cannot run before ratification without contradicting its own preconditions. Conversely, if M-9 is genuinely deferred until after acceptance (as its own annotation states), then the blanket claim "every gating item" completes "before ratification" is imprecise for M-9, and nothing in the Migration Plan specifies who verifies M-9's post-acceptance completion, on what deadline, or via what mechanism (contrast M-6, which explicitly requires a GH Issue + Task + "independently-verified completion" as a named ratification blocker).
**Plausibility:** High — this is a textual property of the deliverable, not a hypothetical.
**Consequence:** Without a comparable verification gate, M-9 risks becoming exactly the kind of "prose table row masquerading as evidence of completion" that the ADR itself warns against for other gating items (L420: "a prose table row is a plan, not evidence of completion"). Since M-9 is explicitly called "the flagship self-compliance demonstration" (ADR L434), an ungated, undeadlined M-9 leaves the convention's single most visible proof-of-concept permanently optional.
**Evidence:** ADR `:420` (blanket "every gating item... before ratification"), `:431` (M-6: "Yes — ratification blocker," GH Issue + Task + independently-verified completion required), `:434` (M-9: "Yes (on acceptance)," TBD-Task only, no GH Issue or verification method specified).
**Dimension:** Internal Consistency; Actionability.
**Mitigation:** Either fold M-9 into the same "before ratification" gate as M-6 (i.e., require the self-promotion to actually execute as part of ratifying the ADR), or explicitly carve out M-9 in the intro sentence ("every gating item, M-6 in particular, except M-9 which gates within N days of acceptance") and give M-9 the same GH Issue + independent-verification treatment as M-6.
**Acceptance Criteria:** The Migration Plan's gating language and M-9's row are mutually consistent, and M-9 has a concrete deadline and verification mechanism equivalent in rigor to M-6's.

---

### IN-005: The null-alternative rebuttal addresses a weak null, not the strongest available one [MAJOR]

**Type:** Assumption
**Original Assumption:** Section "The zero-governance null alternative (requested benchmark, IN-004 [ADR's internal numbering])" establishes that the chosen scheme (B) beats the best available zero-governance alternative.
**Inversion:** Ask what the *strongest* possible zero-governance, maximum-findability alternative would actually look like, and check whether it was tested.
**Plausibility:** High. The rebuttal tested only a "no ID convention + rely on grep/generated index over existing filenames" null (ADR L227-231). It did not test a **CI-generated, content-addressed identity** (e.g., a `ULID`/git-blob-hash-derived ADR ID, assigned automatically at creation and never requiring a human to choose or coordinate a domain slug). Such a scheme would: (a) require **zero** taxonomy governance (no slug to pick, no synonymy risk — directly dissolving IN-002 above); (b) be structurally collision-free (hash/ULID collision probability is negligible, stronger than domain-slug-plus-counter's "mitigated not eliminated" R-6 residual); (c) still support pure-file-move promotion (the ID is content-derived, not scope-derived, so it never needs to change); and (d) require no server process — a CI job that computes and stamps the ID at ADR-creation time is no more "central" than the `sort | uniq -d` step the ADR already relies on for L-3. Confirmed via targeted search: no hash/ULID/UUID/content-addressed option appears anywhere in the six scored options (A-F, `explore/trade-study.md`), the three advocacy documents, or the research survey (`adr-convention-standards-research.md`) — the option space considered was six human-chosen-scope-key variants, not the full space of possible identity mechanisms.
**Consequence:** The claim "B beats the null" (and the associated 0.78 confidence figure) is true against the null actually tested but has not been tested against the strongest available competitor. If a content-addressed scheme would in fact beat B on governance burden (a plausible claim, unrebutted because unconsidered), the decision's confidence level may be overstated for the specific sub-question "is human-chosen taxonomy necessary at all," even though the broader "subject-over-origin" argument (Rationale §1-2, promotion-independent) would likely survive regardless.
**Evidence:** ADR `:225-231` (null-alternative section, tests only "index + grep over existing filenames"); `explore/trade-study.md` (Options A-F, no hash/ULID/generated-index variant, confirmed via search); `projects/PROJ-031-cowork-skeleton/research/adr-convention-standards-research.md` (no hash/ULID/UUID/generated-index mention, confirmed via search).
**Dimension:** Completeness (the requested "invert the goal" benchmark was answered against an incomplete option space); Methodological Rigor.
**Mitigation:** Either add a seventh option (content-addressed/generated ID) to the trade study and score it against the same eight criteria, or explicitly document why it was excluded from scoring (e.g., "opaque IDs lose the discoverability benefit that is force-4's decisive criterion, so a hash scheme was rejected on C4/discoverability grounds without full scoring") so the omission is a disclosed choice rather than an unexamined gap.
**Acceptance Criteria:** The trade study or the null-alternative section explicitly names and scores (or explicitly and reasonedly dismisses) a content-addressed/generated-index alternative before the 0.78 confidence figure is presented as final.

---

### IN-006: Waiver ledger's `approved_by != author` check is a bare string comparison [MINOR]

**Assumption:** The waiver mechanism (rule draft L185) meaningfully prevents self-approval.
**Inversion:** An author self-waives by entering any different name string as `approved_by` (e.g., a colleague's name, without that colleague actually reviewing).
**Consequence:** The lint's stated check ("fails if... `approved_by` equals the commit author") only catches identical-string self-approval, not a fabricated distinct name. Low severity because this is a governance-process gap common to any lightweight file-based waiver system, and the deliverable already improved materially over the prior (bare-comment) design.
**Evidence:** rule draft `:185`.
**Mitigation:** Note as a known limitation, or require `approved_by` to match a second commit's author trailer (e.g., a `Reviewed-by:` git trailer) rather than free text, if stronger assurance is later desired.

### IN-007: Pre-flight collision command is documented but not wired as a hook [MINOR]

**Assumption:** Authors will remember to run the pre-flight `sort | uniq -d` one-liner before committing.
**Inversion:** An author forgets; the collision is caught only at CI (L-3, non-waivable), later than optimal but still before merge.
**Consequence:** Low — this degrades convenience/velocity, not correctness (L-3 remains the backstop). ADR `:326-337`.
**Mitigation:** Wire the one-liner into an optional pre-commit hook, as the ADR itself notes is possible but does not commit to.

### IN-008: The embedded "Inversion check (S-013)" is not a substitute for full S-013 execution [MINOR / INFORMATIONAL]

**Observation:** ADR L399 contains a single paragraph labeled "Inversion check (S-013)" that inverts the top-level A-vs-B choice but does not perform assumption mapping, IN-NNN identifiers, or per-dimension scoring impact — the full methodology this template requires.
**Consequence:** None to this review (this report supplies the full external execution), but future readers should not treat the embedded note as evidence that a rigorous S-013 pass already occurred internally; it is a lightweight self-check, not a completed strategy execution.
**Evidence:** ADR `:399`.
**Mitigation:** None required; noted for traceability only.

---

## Zero-Governance Null Alternative (Explicit Inversion)

The task explicitly asked: *"invert the goal: if we wanted maximum decision-findability with zero governance, what would we do — and does the package beat that null alternative?"*

The deliverable already asks and partially answers this question (ADR L225-231) against a **weak null** ("no convention + search/grep"), and correctly beats it on citation-integrity and collision-safety. This review's inversion goes one step further and identifies a **stronger null the deliverable did not test**: a CI-generated, content-addressed (hash/ULID) ADR identity requiring zero human taxonomy decisions (see [IN-005](#in-005-the-null-alternative-rebuttal-addresses-a-weak-null-not-the-strongest-available-one-major) for the full analysis). Against the null actually tested, the package wins convincingly. Against the untested, stronger null, the outcome is unproven — a disclosed, scoreable gap rather than a refutation of the chosen scheme.

---

## Recommendations

**Critical (MUST mitigate before ratification, M-1):**
- IN-001-20260702iter2 — Reconcile the GOV.UK-vs-"known at birth" contradiction; strengthen D-3's declaration mechanism or explicitly name and monitor the residual Path-2-recurrence risk.

**Major (SHOULD mitigate before ratification):**
- IN-002-20260702iter2 — Add a deterministic (even if WARN-class) lint rule for near-duplicate slug detection; do not rely solely on agent-behavior M-5b.
- IN-003-20260702iter2 — Add an evidentiary-citation exemption to L-8 before this document (or any similar governance ADR) is subjected to the lint.
- IN-004-20260702iter2 — Resolve the M-9 vs. "every gating item... before ratification" contradiction; give M-9 GH-Issue-level verification rigor matching M-6.
- IN-005-20260702iter2 — Score (or explicitly and reasonedly dismiss) a content-addressed/generated-index option in the trade study before treating the null-alternative rebuttal as complete.

**Minor (MAY mitigate):**
- IN-006-20260702iter2, IN-007-20260702iter2, IN-008-20260702iter2 — see individual mitigations above.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-002 (highest-rated own-risk uncovered by lint), IN-005 (option space incomplete against the requested null-alternative benchmark) |
| Internal Consistency | 0.20 | Negative | IN-001 (GOV.UK citation contradicts "known at birth" claim), IN-003 (L-8 vs. document's own evidentiary citations), IN-004 (gating-language contradiction) |
| Methodological Rigor | 0.20 | Negative | IN-001 (core mitigation undermined by the document's own logic), IN-005 (trade study option space narrower than the requested inversion demands) |
| Evidence Quality | 0.15 | Mixed | Overall citation discipline is a genuine strength (nearly every claim in the deliverable is file/line-cited); however IN-003 shows the lint design did not anticipate the document's own evidentiary citation style |
| Actionability | 0.15 | Negative | IN-004 (M-9 lacks a verification mechanism), IN-006 (waiver check weak) |
| Traceability | 0.10 | Neutral-to-Negative | Traceability is otherwise excellent (extensive file:line citations throughout); IN-004's gating ambiguity is the one place where "what counts as ratified" is not fully traceable |

---

## Execution Statistics

- **Total Findings:** 8
- **Critical:** 1
- **Major:** 4
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6 (Goals stated, Anti-goals inverted, Assumptions mapped, Stress-tested, Mitigations developed, Impact synthesized)
- **Anti-goal checklist:** 9 guaranteed-failure conditions checked; 4 cleanly avoided (AG-1..AG-4), 5 live risks identified (AG-5..AG-9)
