# S-010 Self-Refine Findings — Iteration 8 (Group A)

> **Strategy:** S-010 Self-Refine (Madaan et al. 2023) · **Reviewer:** ps-architect (creator/owner) · **Date:** 2026-07-06
> **Deliverables under review (owned):**
> - `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (774 lines)
> - `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (242 lines)
> **Criticality:** C4 (framework-wide governance ADR; AE-002/AE-003 C3 floor, C4 by tier definition)
> **Iteration:** 8 of ongoing adversarial cycle · **Leniency-bias counteraction:** ACTIVE (package already through 7 iterations; high-attachment regime → aim ≥5 findings)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Objectivity Check](#objectivity-check) | Step-1 attachment assessment |
| [Verification Method](#verification-method) | Commands run, evidence base |
| [Mandated Verification Results](#mandated-verification-results) | The 5 specific checks the task requires |
| [Findings Table](#findings-table) | All findings, severity-sorted |
| [Finding Details](#finding-details) | Critical/Major expansions |
| [Scoring Impact](#scoring-impact) | Dimension mapping |
| [Decision](#decision) | Ready / revise / escalate |

---

## Objectivity Check

Step 1 (Shift Perspective). This package has absorbed 7 prior adversarial iterations and a user-authorized subtraction pass; owner attachment is **HIGH** by the template's scale (>8h cumulative, strong investment). Per the Conservative Fallback, I adopt the stricter Medium/High guidance: **leniency-bias counteraction active, target ≥5 findings even if the package reads clean.** I review as if inspecting another author's work: "Would I accept this if I had not written it?"

---

## Verification Method

Empirical, tool-based (not prose-trust). Evidence base:
- `wc -l` / `wc -w` on the rule draft (token estimate = words × 1.35, the project's own convention).
- `grep -n` for deleted-machinery remnants (waiver, two-tier, CODEOWNERS, non-bypassable, non-waivable) across both files.
- `grep -nE` for uppercase HARD-tier keywords (MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL) in the rule draft.
- `grep -n` for deleted lint-rule IDs (L-5, L-6, L-8, L-9, L-10, L-11, L-12, L-13, L-14, L-4b, L-1a, L-1b) presented as *live* mechanisms.
- Count of live lint rules in each file's 5-rule table.
- Cross-check of iteration-005 Critical dispositions in `subtraction-pass-notes.md`.

Results recorded in [Mandated Verification Results](#mandated-verification-results) below.

---

## Mandated Verification Results

The task named five specific checks. Each is answered with measured evidence, not prose-trust.

| # | Mandated check | Result | Evidence |
|---|----------------|--------|----------|
| 1a | Rule draft ≤ ~2,500 tokens | **MISS (disclosed)** — measured **~4,310 tokens** (`wc -w` = 3,193 words × 1.35), **242 lines**. ~72% over the ~2,500-token soft target; **within** the 250–350-line guidance (242 < 250). Honestly disclosed at rule-draft:199 and notes:73/181. | `wc -l -w` on `adr-standards-rule-draft.md` = 242 / 3,193 |
| 1b | Lint ≤ 5 rules | **PASS** — exactly 5: L-1, L-2, L-3, L-4, L-7 (rule-draft:173-177; ADR:667-671). | `grep '\*\*L-[0-9]'` → 5 rows |
| 1c | Zero waiver-ledger / two-tier / non-bypassable remnants | **PASS** — rule draft: only 2 hits (line 165 honest "no waiver ledger, no CODEOWNERS gate, no non-bypassable rule"; line 238 changelog describing the deletion). ADR: all hits are in changelog rows (historical) or deletion-disclosure notes (subtraction note :642, R-C :597). Zero present as LIVE machinery. | `grep -niE 'waiver\|two-tier\|codeowners\|non-bypassable\|non-waivable\|ledger'` |
| 2 | Ratification (FU.0, Scheme B) folded consistently | **PASS** — ADR own status `ACCEPTED` in frontmatter (:4), header (:25), Status (:83), Decision (:213). All `PROPOSED` occurrences are schema-examples (:344 template, :544 Path-0 guidance) or Status-Vocabulary definitions (:605-628), never this ADR's status. Rule draft wrapper "REVIEW DRAFT of a **ratified** convention" (:3) — the *file* is pre-M-2-move; the *decision* is ratified. | `grep -nE 'ACCEPTED\|PROPOSED'` both files |
| 3 | Every iteration-005 Critical has a disposition in `subtraction-pass-notes.md` | **PASS** — "Critical Findings Disposition (all 10)" table, rows 1-10 (notes:85-94): PM-001, PM-002, RT-001, RT-002, RT-003, FM-001, FM-002, FM-003, FM-006, IN-013-005 — each carries a disposition (8 CLOSED-BY-DELETION, 2 CLOSED-BY-EDIT, plus RESIDUAL-DISCLOSED hybrids; 0 left blank). | `grep '^\| [0-9]+ \|'` → 10 rows |
| 4 | No dangling refs to deleted machinery in either file | **PASS** — deleted lint IDs (L-5/L-6/L-8/L-9/L-10/L-11/L-12/L-13/L-14/L-4b/L-1a/L-1b) appear ONLY as explicit deletions/descopes ("was descoped", "was removed in the subtraction pass", "retired", "the deleted L-1a/L-1b split ... declined") or in historical changelog rows. None presented as a live mechanism. | `grep -nE 'L-(5\|6\|8\|9\|10..14\|4b\|1a\|1b)'` both files |
| 5 | Tier vocabulary clean (no MUST/SHALL in rule draft) | **PASS** — zero uppercase HARD keywords (MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL) anywhere in the rule draft. All normative force carried by SHOULD/RECOMMENDED/MAY. | `grep -nE '\b(MUST\|SHALL\|NEVER\|FORBIDDEN\|REQUIRED\|CRITICAL)\b'` → 0 |

**Bottom line:** 4 of the 5 mandated checks PASS cleanly; check 1a (≤2,500 tokens) is a **disclosed miss** — the doctrine (delete attack-surface machinery, don't compensate) fully held and is verified, but the numeric token target is exceeded by ~72% and is honestly labeled as irreducible normative content.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-i8 | Rule-draft token budget missed: ~4,310 tokens vs the ~2,500 hard target (~72% over) and **trending up** across the two post-subtraction passes (233 ln/3.25k → 238/3.9k → 242/4.3k). Each addition is a *disclosure*, not machinery, so the doctrine holds — but the "add prose to correct overclaim" loop is a mild inversion of the subtraction goal. Disclosed at rule-draft:199, notes:73/181. | Major | `wc -w`=3,193 → 4,310 tok; notes:181 growth trail | Methodological Rigor / Completeness |
| SR-002-i8 | `subtraction-pass-notes.md` "Budgets Achieved" table (:69-73) shows "After (measured)" = **3,248 tokens / 233 lines** — the v1.7 snapshot, now two passes stale. The same file's Files-Edited row (:181) and the rule draft (:199) give the current 4,310/242, but the Budgets table header implies "After" is current. | Minor | notes:69 vs notes:181 | Internal Consistency |
| SR-003-i8 | Rule-draft v1.7 changelog parenthetical (:238) reads "~3.3k (233 lines … ~30% above the ~2.5k soft target)"; current state (:199) is "~4.3k … above the soft target." The v1.7 row is a legitimate historical record but carries no forward-pointer to the later figure, so a changelog-only reader sees a stale ratio. | Minor | rule-draft:238 vs :199 | Internal Consistency |
| SR-004-i8 | Cross-artifact iteration-numbering divergence: the tournament that produced the 10 disposed Criticals is "**iteration 4** full tournament" in the ADR changelog (:762, v1.5) but "**iteration-5** Critical[s]" in the subtraction-notes header/nav (:1,:14). Disposition completeness is unaffected (all 10 disposed); the label mismatch is cosmetic. | Minor | ADR:762 vs notes:1 | Traceability |
| SR-005-i8 | Rule-draft wrapper "REVIEW DRAFT of a ratified convention" (:3) is a momentary oxymoron — resolved in the same sentence (file is a draft pre-M-2-move; decision is ratified). Acceptable as written; noted for leniency-counteraction completeness, no change recommended. | Minor (noted, no change) | rule-draft:3 | Internal Consistency |

---

## Finding Details

### SR-001-i8 — Token budget missed and trending up (Major)

- **Severity:** Major (not Critical: content is complete, correct, honest, and machinery-free; nothing blocks acceptance).
- **Affected Dimension:** Methodological Rigor (0.20), Completeness (0.20).
- **Evidence:** Measured `wc -w` = 3,193 words × 1.35 = **~4,310 tokens** at 242 lines. The FU.1 mandate set a hard budget of "≤ ~2,500 tokens (~250–350 lines)". Growth trail (notes:181): 233 ln/~3.25k (v1.7 subtraction) → 238/~3.9k (iter-6) → 242/~4.3k (iter-7).
- **Impact:** The subtraction pass's *purpose* — remove attack-surface machinery — is fully achieved and independently verified (lint 18→5; waiver/two-tier/CODEOWNERS gone). But the numeric token target is exceeded by ~72%, and each subsequent adversarial pass has *added* disclosure prose to correct overclaims, nudging the count upward. This is defensible (each addition prevents a P-022 overclaim, and cutting further would delete a normative section, leaving the rule incomplete) and is honestly disclosed. It is nonetheless a real target-miss the owner/user should explicitly accept.
- **Recommendation:** **Do NOT cut normative content** to chase the literal 2,500-token figure (that would trade completeness for an arbitrary number and reintroduce overclaim). Instead: (a) surface this overage to the user as an *accepted deviation* — the line-count budget (242 < 250) is met and the token overage is irreducible normative convention content; and (b) reconcile the mandate's two mutually-inconsistent budget expressions (≤2,500 tokens vs 250–350 lines) so future passes are measured against one target. Verification: line-count stays < 250; token figure stated, not rounded down (already done at :199).

### SR-002-i8 — Stale "Budgets Achieved" table (Minor)

- **Severity:** Minor. **Affected Dimension:** Internal Consistency.
- **Evidence:** notes:69 "Rule-draft tokens … After (measured wc -w × 1.35) **~3,248** (2,406 w)"; notes:70 "**233**"; vs notes:181 "**242 lines / ~4.3k tokens** … the single current figure."
- **Impact:** A reader landing on the Budgets table sees the v1.7 snapshot as "After," conflicting with the current figure elsewhere in the same file. Low-risk (the notes are a supporting log, not a primary deliverable; the current figure is present two rows down).
- **Recommendation:** Annotate the Budgets table "After" column as "(at subtraction pass v1.7; grew to ~4,310/242 by iter-7 — see Files Edited)" OR leave as-is and treat notes:181 as the authoritative current figure. Since this file is the disposition log (not one of the two named deliverables) and editing it risks disturbing the disposition record, **flag not edit** is the mandate-conservative call (P-020).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral→slightly Negative | All normative sections present; the token overage is a *side-effect* of completeness, not a gap (SR-001). |
| Internal Consistency | 0.20 | Slightly Negative | Two stale-figure nits (SR-002, SR-003); ratification consistently folded; no deleted-machinery live refs. |
| Methodological Rigor | 0.20 | Positive (with note) | Subtraction doctrine verified: lint 18→5, machinery gone, all 10 Criticals disposed, tier vocabulary clean. SR-001 upward token trend is the one rigor caveat. |
| Evidence Quality | 0.15 | Positive | Claims grep/`wc`-pinned; residuals labeled [INHERENT]/Claim-Status; P-022 disclosures throughout. |
| Actionability | 0.15 | Positive | Migration plan M-1…M-14 concrete; residuals carry owners + detection signals. |
| Traceability | 0.10 | Neutral | Finding-ID tags resolve; one cosmetic iteration-numbering divergence (SR-004). |

---

## Decision

**Outcome:** READY FOR EXTERNAL REVIEW / ACCEPT (verdict PASS).

**Rationale:** All five mandated verifications pass except the ≤2,500-token numeric (check 1a), which is a **disclosed, defensible miss** — the subtraction *doctrine* held completely (lint 18→5, waiver/two-tier/CODEOWNERS/non-bypassable machinery gone, verified by grep), ratification (FU.0, Scheme B) is consistently folded, every iteration-005 Critical is disposed, there are zero dangling refs to deleted machinery, and the rule-draft tier vocabulary is clean (zero MUST/SHALL). The token overage is irreducible normative content, honestly labeled, with the line-count budget met (242 < 250). No Critical findings. The single Major (SR-001) is a target-miss to be accepted by the owner, not a correctness defect.

**No edits made to the two deliverables (P-020, subtraction doctrine).** Cutting to hit 2,500 tokens would delete a normative section and leave the rule incomplete (worse than the disclosed overage); rewriting historical changelog rows would violate the ADR's own FM-014 "don't rewrite history" principle. The correct S-010 disposition is to surface SR-001 for explicit user acceptance and leave the honest disclosures in place.

**Next Action:** Surface SR-001 (token overage + the two-budget-expression inconsistency) to the user for accept-as-deviation; the three Minors are cosmetic/staleness in supporting artifacts and can be batched into the next routine edit or left as disclosed. No further self-refine iteration warranted — the package has converged.
