# Devil's Advocate Report: ADR-PROJ031-004 + Companion Rule Draft (Iteration 6, Post-Subtraction)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverables, H-16 status |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All DA-NNN findings at a glance |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |
| [Notes on Scope and Method](#notes-on-scope-and-method) | Blind-protocol compliance, what was and was not read |

---

## Execution Context

**Strategy:** S-002 Devil's Advocate
**Deliverables:**
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (751 lines, read in full)
- `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (233 lines, read in full)
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-05
**Reviewer:** adv-executor (blind, independent)
**Iteration:** 6 (post-subtraction pass, per `orchestration/adr-convention-20260702-001/subtraction-pass-notes.md`)

**H-16 Compliance:** S-003 Steelman is not separately re-run this iteration, but H-16 evidence is directly present and verifiable in the deliverable itself: (a) `ADR-PROJ031-004-adr-identifier-convention.md:65-68` documents an explicit S-003 traceability note (`ST-001`, `ST-002` tags) and states the Steelman work product is embedded in each Option A-F's "Strongest case" framing (`ADR-PROJ031-004-adr-identifier-convention.md:150,158,166,174,182,189` — one per scheme); (b) three standalone advocate documents exist under `explore/` (`advocate-project-scoped.md`, `advocate-domain-slug.md`, `advocate-external.md`), confirming genuine pre-critique strengthening occurred earlier in this engagement. This is treated as H-16-satisfied for the purpose of this iteration's Devil's Advocate pass; per P-022 this reviewer cannot independently confirm an iteration-6-specific discrete S-003 artifact exists (none was presented), and does not claim that it does.

**Mandate compliance:** Per the invoking task, this review evaluates the package **as it now stands** post-subtraction. Findings below do not re-litigate the deliberate removal of machinery (waiver ledger, two-tier ratification, 13-of-18 lint rules) as a category — descoping is accepted as a valid MEDIUM-tier posture. The attack surface examined is narrower and sharper: (1) does the retained 5-rule core actually deliver the collision-safety the documents claim it delivers, (2) was anything quietly load-bearing among the deletions, and (3) is the "descoped, honestly" list actually complete, or does it omit residuals that should have been named alongside R-1 through R-8.

---

## Summary

The subtraction pass is honest about *most* of what it removed, but two of the deletions/gaps are not honest by omission: the sole retained collision-detection mechanism (L-3 / the "pre-flight" `sort | uniq -d` one-liner) is textually and functionally scoped to **canonical** lowercase domain-slug IDs only, and structurally cannot detect a duplicate within the **dialect** family (`PROJ|EPIC|FEAT|STORY`) — which is exactly the ID class of this ADR's own headline collision anecdote (`ADR-EPIC002-001`). Separately, the deleted rule L-9 ("block new files under frozen dirs") leaves the explicit claim "Frozen sets... are closed to new entries" (rule draft:94) with no enforcing mechanism at all, and this gap appears nowhere in the otherwise-thorough Descoped/Residuals/Risks disclosure. A third finding shows the subtraction pass's own disposition arithmetic (12 named deleted rules vs. a claimed "13 of 18") does not reconcile from the evidence given. **6 findings total: 2 Critical, 2 Major, 2 Minor. Recommendation: REVISE** — the Critical findings are narrow and each has a low-cost fix (a regex extension or a one-line rule restoration / honest re-scoping), but until addressed, the "collision-safety" and "frozen = closed" claims are overstated relative to what the retained mechanism actually checks.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter006 | L-3 (and the pre-flight one-liner it is declared identical to) only extracts canonical lowercase `{domain-slug}-NNN` IDs; it structurally cannot see dialect (`PROJ\|EPIC\|FEAT\|STORY`) duplicates — the exact class of this ADR's own motivating collision (`ADR-EPIC002-001`) | Critical | `ADR-PROJ031-004-adr-identifier-convention.md:394,398,653`; `adr-standards-rule-draft.md:173,179,185`; `ADR-PROJ031-004-adr-identifier-convention.md:113` | Methodological Rigor, Completeness |
| DA-002-iter006 | Deletion of L-9 ("block new files under frozen dirs") leaves the rule draft's explicit claim "Frozen sets... are closed to new entries" with zero enforcing mechanism, and this gap is not listed among the Descoped/Residuals/Risks disclosures | Critical | `subtraction-pass-notes.md:56`; `adr-standards-rule-draft.md:66,94,172`; `ADR-PROJ031-004-adr-identifier-convention.md:738` (v1.2 changelog naming L-9's original purpose); `adr-standards-rule-draft.md:191` (Descoped note, no mention); `ADR-PROJ031-004-adr-identifier-convention.md:442-453` (Risks table, no mention) | Internal Consistency, Completeness |
| DA-003-iter006 | Subtraction pass's own disposition arithmetic does not reconcile: 12 lint-rule IDs are named as deleted while the same document claims "13 of 18," and the 5 retained rules are described as the "fail-closed core" against an original "12 FAIL + 6 WARN" split (12−5=7 FAIL deletions needed, only 6 accounted for in the named list plus 6 WARN = 12, not 13) | Major | `subtraction-pass-notes.md:56,70,74` | Traceability, Internal Consistency |
| DA-004-iter006 | "Periodic audit" / "periodic listing review" is asserted twice as a taxonomy-synonymy risk mitigation, but the only actual Migration-Plan action item (M-5b) defines an at-authoring-time eyeball check with no cadence, owner, or trigger — unlike the comparably-scoped R-6 risk, which gets a concrete numeric threshold | Major | `ADR-PROJ031-004-adr-identifier-convention.md:448,472,507` | Actionability, Evidence Quality |
| DA-005-iter006 | L-4's rule text enumerates only `PROJ{NNN}/EPIC{NNN}/STORY{NNN}` for the ID-location check, omitting `FEAT` despite FEAT being part of the closed dialect prefix set declared elsewhere in both documents | Minor | `adr-standards-rule-draft.md:174`; `ADR-PROJ031-004-adr-identifier-convention.md:651,324-329` | Internal Consistency |
| DA-006-iter006 | The claim "collision/grammar rules are rarely overridden because a compliant NNN/slug is always available" is stated as a flat behavioral prediction with no evidence or hedging, inconsistent with this document's otherwise-careful practice of labeling predictions as inference (P-022) | Minor | `adr-standards-rule-draft.md:165` | Evidence Quality |

---

## Finding Details

### DA-001: Collision-safety claim does not cover the ID class that motivated the whole ADR [CRITICAL]

**Claim Challenged:** The rule draft states L-3 "Extract `{slug}-NNN` of all non-frozen ADRs; `sort \| uniq -d` must be empty. **Repo-wide.**" (`adr-standards-rule-draft.md:173`). The ADR independently asserts "the pre-flight collision one-liner... is exactly what L-3 runs in CI" (`ADR-PROJ031-004-adr-identifier-convention.md:653`), and the rule draft makes the identical claim (`adr-standards-rule-draft.md:179`, "exactly what L-3 runs in CI"). Both documents therefore present this mechanism as the authoritative, repo-wide collision-safety guarantee for the whole convention.

**Counter-Argument:** The command's own inline comment restricts its scope explicitly: `# Lists any canonical {domain-slug}-NNN identity used by more than one non-frozen ADR.` (`ADR-PROJ031-004-adr-identifier-convention.md:394`). The extraction regex confirms this narrowing is not cosmetic: `grep -E '^ADR-[a-z0-9-]+-[0-9]{3}'` (`ADR-PROJ031-004-adr-identifier-convention.md:398`; identical at `adr-standards-rule-draft.md:185`). The character class `[a-z0-9-]+` matches only lowercase letters, digits, and hyphens. A dialect ID such as `ADR-PROJ031-005` or `ADR-EPIC002-001` contains uppercase letters (`P`, `R`, `O`, `J`, `E`, `P`, `I`, `C`) immediately after `ADR-`, which the regex's character class does not admit — the line is silently dropped before it ever reaches `sort | uniq -d`. The mechanism therefore checks **canonical (lowercase domain-slug) IDs only**, contradicting the "of all non-frozen ADRs... Repo-wide" framing in the rule spec, which implies universal coverage.

This is not a hypothetical gap. The ADR's own central, repeatedly-cited real-world collision example — used as the primary evidentiary anchor for why a convention is needed at all — is `ADR-EPIC002-001`, "independently re-minted for the output-path-resolution decision, colliding with the pre-existing, SSOT-cited `ADR-EPIC002-001-strategy-selection`" (`ADR-PROJ031-004-adr-identifier-convention.md:113`). That is an entity-ID/dialect-family collision (`EPIC002`), not a canonical-domain-slug collision. Under the retained L-3 mechanism as literally written, that exact identity string would never be extracted, would never reach `sort | uniq -d`, and the collision would **not** have been flagged. Since the dialect grammar remains permitted going forward (D-3, SOFT `MAY`) and is not deprecated, a repeat of the exact founding incident is currently undetectable by the sole surviving fail-closed collision mechanism.

**Impact:** The document's headline claim — that the slimmed 5-rule core still "delivers collision-safety" — is materially overstated for the dialect ID family, which is (a) still permitted, (b) the source of the one demonstrated real collision in the corpus, and (c) not covered by any other rule (L-4 checks location-consistency, not NNN uniqueness).

**Dimension:** Methodological Rigor (the mechanism does not match its stated scope), Completeness (a permitted ID family has zero collision coverage).

**Response Required:** Either (a) extend the L-3 extraction to also catch dialect-family duplicates (e.g., a second regex pass or case-insensitive normalization keyed on the closed `{PROJ|EPIC|FEAT|STORY}\d{3}-\d{3}` pattern), or (b) explicitly narrow the "collision-safety" claim in both documents to "canonical IDs only" and add dialect-duplicate risk as a named, disclosed residual parallel to R-6/R-7, rather than leaving the "of all non-frozen ADRs... Repo-wide" language standing uncorrected.

**Acceptance Criteria:** The retained lint spec's stated scope (prose) and its actual regex (mechanism) agree with each other, and whichever is true is verifiably true against the `ADR-EPIC002-001` historical incident (i.e., re-running the corrected mechanism against that exact pre-rename filename pair would flag it).

---

### DA-002: Deleting L-9 leaves "frozen = closed to new entries" as an unenforced, undisclosed claim [CRITICAL]

**Claim Challenged:** "**Frozen** sets (`docs/adrs/`, `docs/archive/`) are closed to new entries." (`adr-standards-rule-draft.md:94`). The ID Scheme section reinforces this: "**Frozen**: `ADR-NNN`/`ADR-0NN` in `docs/adrs/`, `docs/archive/` (do not extend)." (`adr-standards-rule-draft.md:66`).

**Counter-Argument:** In the 18-rule design, this guarantee was enforced by a dedicated rule, added specifically for this purpose: the ADR's own v1.2 changelog records "(P0-6/RT-002) added non-waivable **L-9** (block *new* files under frozen dirs)" (`ADR-PROJ031-004-adr-identifier-convention.md:738`). The subtraction pass's Step 2 table lists `L-9` among the "13 of 18 lint rules" deleted (`subtraction-pass-notes.md:56`), with no individual replacement or carve-out.

Examining the 5 retained rules confirms nothing fills the gap. L-2 ("No new bare") explicitly **exempts** frozen dirs from its check: "A git-added file must not match `^ADR-\d`, anywhere **except frozen dirs** (`docs/adrs/`, `docs/archive/`)." (`adr-standards-rule-draft.md:172`). L-1 (grammar) is scoped only to `projects/*/decisions/` and `docs/design/` (`adr-standards-rule-draft.md:171`) and does not apply to `docs/adrs/`/`docs/archive/` at all. L-3, L-4, and L-7 are collision, location, and relationship checks respectively — none constrains *whether a new file may be added* to a frozen directory. The practical result: a new bare-numbered file (`ADR-999-foo.md`) — or, for that matter, any file matching `ADR-*.md` — can be added to `docs/adrs/` or `docs/archive/` today without failing any of the 5 retained rules, directly contradicting "closed to new entries."

This gap is not disclosed. The "Descoped, honestly" note in both documents (`adr-standards-rule-draft.md:191`; `ADR-PROJ031-004-adr-identifier-convention.md:655`) lists seven specific omitted checks (provenance WARNs, citation scanning, taxonomy-synonymy matching, producer-drift monitoring, supersession separation-of-duties, repository-topology dialect rejection) — but not this one. The Risks table (`ADR-PROJ031-004-adr-identifier-convention.md:442-453`, R-1 through R-8) has no entry for it either. This is precisely the class of gap the document elsewhere prides itself on catching and naming (e.g., the FM-001 retraction of an overstated L-8 backstop claim) — but this one survived the subtraction pass unnoticed.

**Impact:** "Frozen" is the mechanism specifically meant to prevent the bare-`ADR-NNN` collision pattern (which the ADR itself documents colliding three times, `ADR-PROJ031-004-adr-identifier-convention.md:97-113` family table) from recurring in the one place it already happened. Removing the sole enforcement of "no new entries" without disclosure re-opens exactly that door, silently.

**Dimension:** Internal Consistency (explicit prose claim contradicted by the actual mechanism), Completeness (a stated guarantee has no enforcing rule).

**Response Required:** Either restore a minimal check (a one-line addition — e.g., have L-1 or L-2 flag any *newly git-added* file under `docs/adrs/`/`docs/archive/` against a pre-adoption allowlist, rather than exempting frozen dirs unconditionally) or correct "closed to new entries" to "closed by convention, not lint-enforced in the 5-rule core" and add it to the Descoped note and Risks table alongside R-1..R-8.

**Acceptance Criteria:** Either a demonstrable rule blocks a new file being added to a frozen directory, or the prose no longer claims that outcome is enforced, and the gap is listed as a named, owned residual.

---

## Finding Details (Major — Abbreviated per Template §4 scope; Critical findings above receive full expansion, Major findings below receive condensed detail per evidence density)

### DA-003: The subtraction pass's own rule-deletion count does not reconcile [MAJOR]

**Claim Challenged:** "Lint cut 18→5 rules" is asserted repeatedly (`adr-standards-rule-draft.md` Changelog v1.7; `ADR-PROJ031-004-adr-identifier-convention.md` Changelog v1.7). The authoritative disposition record for this claim, cited by name in both deliverables' changelogs ("Full disposition: `../orchestration/adr-convention-20260702-001/subtraction-pass-notes.md`"), states: "**13 of 18 lint rules** (L-4b, L-5, L-6, L-6b, L-6c, L-8, L-9, L-10, L-11, L-12, L-13, L-14)" were deleted (`subtraction-pass-notes.md:56`).

**Counter-Argument:** The parenthetical names exactly 12 rule IDs, not 13. Cross-checked against the Budgets Achieved table in the same file — "L5 lint fail-closed rules | ≤ 5 | **18 (12 FAIL + 6 WARN, growing)** | **5**" (`subtraction-pass-notes.md:70`) and "The 5 retained rules are the highest-value **fail-closed** set" (`subtraction-pass-notes.md:74`, implying all 5 retained were originally FAIL-tier) — the arithmetic requires 12 FAIL − 5 retained = 7 FAIL-tier deletions, plus 6 WARN-tier deletions, for 13 total. The named list, however, contains at most 6 plausible WARN-candidates (L-5, L-6, L-6b, L-6c, L-10, L-14) and 6 plausible FAIL-candidates (L-4b, L-8, L-9, L-11, L-12, L-13) = 12, one short of the 7 FAIL-tier deletions the math requires. One deleted rule is therefore unaccounted for by ID in the very table whose stated purpose is per-rule justification ("Findings it closes"). *(Labeled as inference, not fact, per P-022: a plausible innocent explanation is an earlier-iteration consolidation of a previously-separate `L-1a`/`L-1b` split — referenced at `ADR-PROJ031-004-adr-identifier-convention.md` v1.1 changelog, "split the L-1 lint into disjunctive L-1a canonical / L-1b uppercase-dialect" — back into the single unified `L-1` now shown. If so, that merge is a legitimate architectural consolidation, not a "deletion," but it is not stated anywhere in the disposition record, so the "13 of 18" claim cannot be verified as accurate from the documents as given.)*

**Impact:** Undermines the "no Critical left without a disposition... full disposition" completeness claim (`subtraction-pass-notes.md:78-97`) for the lint-rule inventory specifically — a smaller-scope but structurally identical defect to the count-reconciliation errors this same document elsewhere prides itself on catching (SM-201, CV-001-style corrections in the ADR's own changelog).

**Dimension:** Traceability, Internal Consistency.

**Response Required:** Name the 13th deleted rule explicitly, or correct "13 of 18" to the verifiable count, in the disposition record both deliverables cite as authoritative.

**Acceptance Criteria:** The count of named-deleted rules, retained rules, and any disclosed consolidations sums to the stated original total (18) without an unstated step.

### DA-004: "Periodic audit" is asserted as a mitigation with no defined mechanism [MAJOR]

**Claim Challenged:** The Risks table lists, for R-3 (taxonomy synonymy): "Domain index + lightweight arbiter (TBR-2); **periodic audit**." (`ADR-PROJ031-004-adr-identifier-convention.md:448`). The Pre-Mortem table's FM-4 containment column likewise states: "**Periodic** `docs/design/` listing review; index drift" (`ADR-PROJ031-004-adr-identifier-convention.md:472`).

**Counter-Argument:** The only Migration-Plan action item that operationalizes this (M-5b) describes solely an at-authoring-time, ad hoc check: "new slugs SHOULD be eyeballed against it and the `projects/*/decisions/` set for near-duplicates... **at authoring time**." (`ADR-PROJ031-004-adr-identifier-convention.md:507`). No cadence, no trigger, no named periodic review point, and no owner-of-the-periodic-step is defined anywhere — "periodic" appears only as an adjective in the risk/pre-mortem framing, never as a scheduled activity in the plan that is supposed to deliver it. This is a materially lower bar than the rigor the document applies to its comparably-scoped residual R-6 ("cross-branch same-slug NNN race"), which gets a precise, falsifiable threshold: "`≥ 2` distinct L-3 collision failures on `main` within any rolling 90-day window" (`ADR-PROJ031-004-adr-identifier-convention.md:457`). R-3/FM-4's "periodic audit" gets no equivalent operationalization.

**Impact:** A reader relying on the Risks/Pre-Mortem tables would reasonably conclude a scheduled review process exists; it does not. This is the same class of gap (asserted mitigation, no actual mechanism) that the FM-001 retraction elsewhere in this same document was created specifically to eliminate.

**Dimension:** Actionability (no verifiable response mechanism), Evidence Quality (claim not backed by the plan it points to).

**Response Required:** Either add a concrete cadence/owner/trigger for the taxonomy review (matching R-6's rigor), or replace "periodic audit"/"periodic listing review" in the Risks and Pre-Mortem tables with the accurate description already used at M-5b: "best-effort, at-authoring-time review only."

**Acceptance Criteria:** Every occurrence of "periodic" applied to taxonomy review either points to a defined cadence or is removed in favor of the accurate at-authoring-time framing.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- **DA-001:** Extend L-3's extraction to cover dialect-family duplicates, or explicitly narrow the collision-safety claim to canonical IDs and disclose dialect-duplicate risk as a named residual. Acceptance criteria as stated above.
- **DA-002:** Restore minimal enforcement for "no new entries in frozen dirs," or correct the prose claim and add it to the Descoped/Risks disclosure. Acceptance criteria as stated above.

**P1 (Major — SHOULD resolve; require justification if not):**
- **DA-003:** Reconcile the "13 of 18" lint-rule deletion count in `subtraction-pass-notes.md:56` against the named IDs and the FAIL/WARN split at `:70`.
- **DA-004:** Define a concrete cadence/owner for the taxonomy "periodic audit," or downgrade the claim to match M-5b's actual at-authoring-time scope.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- **DA-005:** Add `FEAT` to L-4's prose enumeration in both documents, matching the closed dialect set declared in the ID grammar section.
- **DA-006:** Hedge the "rarely overridden because a compliant NNN/slug is always available" claim (`adr-standards-rule-draft.md:165`) consistent with this document's general P-022 practice of labeling predictions as such.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-001, DA-002: two coverage gaps (dialect-duplicate detection, frozen-dir new-entry blocking) exist in the retained mechanism set but are not named as residuals. |
| Internal Consistency | 0.20 | Negative | DA-002 (prose vs. mechanism contradiction), DA-003 (disposition arithmetic), DA-005 (FEAT omission inconsistent with the declared closed set). |
| Methodological Rigor | 0.20 | Negative | DA-001: the sole retained collision-detection mechanism does not structurally cover the ID class of the document's own motivating incident. |
| Evidence Quality | 0.15 | Negative | DA-004 (mitigation asserted without a backing mechanism), DA-006 (unhedged behavioral prediction). |
| Actionability | 0.15 | Negative | DA-004: no cadence/owner/trigger defined for a claimed periodic review. |
| Traceability | 0.10 | Negative | DA-003: the cited "full disposition" record's own count does not reconcile. |

**Result:** 6 findings (2 Critical, 2 Major, 2 Minor) across 6 of 6 scoring dimensions, all Negative-impact. Both Critical findings are narrow, well-evidenced, and each has a low-cost remediation path (a regex extension / one-line rule restoration, or an honest re-scoping of the corresponding claim). **Overall assessment: REVISE.** The subtraction pass's core doctrine (delete machinery rather than compensate) is sound and mostly executed honestly, but the two Critical findings show the doctrine was not applied with full verification against the retained mechanisms' actual behavior — the "collision-safety" and "frozen = closed" claims currently promise more than the 5-rule core delivers.

---

## Notes on Scope and Method

- Read in full: both deliverables (`ADR-PROJ031-004-adr-identifier-convention.md`, 751 lines; `adr-standards-rule-draft.md`, 233 lines), `subtraction-pass-notes.md` (155 lines, explicitly permitted as owner disposition evidence), and the `explore/` directory listing (advocate documents, confirmed present but not opened in detail beyond confirming their existence for the H-16 check).
- Not read: any other file under `orchestration/adr-convention-20260702-001/adversary/` (blind-protocol compliance) — no prior iteration's findings, remediation notes, or other strategies' outputs informed this report.
- No edits made to either deliverable (owner-only edit rights respected, P-020).
- No subagents spawned (P-003).
- All findings cite file and line number against the two deliverables plus the explicitly-permitted evidence file; the one inference (DA-003's possible L-1a/L-1b merge explanation) is labeled as such, not asserted as fact (P-022).
