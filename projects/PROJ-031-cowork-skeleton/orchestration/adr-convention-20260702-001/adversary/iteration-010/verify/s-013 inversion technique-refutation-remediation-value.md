# Refutation Panel — Remediation-Value Lens — S-013 Inversion Technique (iteration 10)

> Panel: adv-executor (blind, single-lens). Lens: **remediation-value** — would fixing this materially change real adoption outcomes, or is it churn?
> Target report: `s-013-findings.md` (iteration-010).
> Scope: Critical findings only, per mandate. The report contains exactly one Critical (013-001); 013-002 is Major and out of scope for this panel.

---

## Verdict Table

| Finding ID | Severity (as reported) | Verdict | One-line reason |
|---|---|---|---|
| 013-001 | Critical | **REFUTED** | The claimed "contradiction" is already resolved, in-section, by (a) the table's own header caveat and (b) the immediately-adjacent IN-001-iter8 paragraph that explicitly operationalizes the grandfather-baseline exemption for exactly the `ADR-150-001` case. The proposed fix is cosmetic text-merging, not a substantive spec gap, and the underlying issue was already disposed once (iteration-8, IN-001) via this exact wording. |

---

## Reasoning: 013-001 — REFUTED

**Claim under test:** that L-1's row definition ("Filename matches canonical OR dialect") and the mandatory grandfather regression test ("18 files pass L-1") are irreconcilably contradictory for `ADR-150-001`, because the grandfather-baseline exemption is stated only as free-standing prose *after* L-1's row and is "never folded back into L-1's own stated test."

**Why this is refuted on remediation-value grounds:**

1. **The table header itself already scopes every row, including L-1, to non-grandfathered files.** Both documents place this caveat directly above the L-1/L-2/L-3/L-4/L-7 table: "Rule | Checks (git-added/modified files; **pre-adoption grandfathered**)" (ADR:684, rule-draft:173, restated verbatim). This is not buried — it is the column header the finder's own quoted row sits under. A reader (or implementer) encountering the L-1 row cannot avoid seeing this qualifier in the same visual unit as the row. The finder's reproduced quotes (ADR:686, rule-draft:175) isolate the row's rejection sentence from this header, which is what manufactures the appearance of an unqualified assertion.

2. **The very next paragraph in the same subsection is titled to answer exactly this question, and does so in implementer-actionable terms.** ADR:693 / rule-draft:183 ("IN-001-iter8 spec clarification... L-1 wording, not a sixth rule") states plainly: grandfathering is resolved against a static ratification-time baseline; a file already on that baseline is "grandfathered-exempt from L-1/L-2, not as newly-minted"; and it names `ADR-150-001` explicitly as the case this closes ("the numeric-leading legacy `ADR-150-001`... would FAIL L-1... With the baseline, only files absent from it are held to L-1/L-2 as 'new'"). This is not an orphaned aside — it is the direct continuation of the grandfather-regression-test paragraph (ADR:691) that the finder itself cites as creating the "unsatisfiable gate." An implementer reading the L5 CI Lint Specification section top-to-bottom (table -> grandfather-test paragraph -> IN-001-iter8 clarification, three consecutive blocks) has a complete, unambiguous, three-way-disjunction specification for L-1's actual runtime behavior. The finder's own evidence list (013-001, bullet on ADR:693) concedes this text exists and says what the finder wants it to say — the objection is purely that it is not copy-pasted into the row cell itself.

3. **This is not "genuine and previously undisclosed" — it is a re-litigation of an issue already closed by this exact wording.** `subtraction-pass-notes.md` iteration-8 disposition table (lines 194, 213-221 region) records: "IN-001 | S-013 | ... **CLOSED-BY-EDIT** | Grandfather clause added to L-1's spec text... so a later-edited legacy file (`ADR-150-001`) is exempt rather than new-bare, closing the deleted-L-12 gap by wording (IN-001)." That is the *same* S-013 strategy, the *same* file (`ADR-150-001`), and the *same* mechanism (L-12 reattachment via L-1 spec wording) that 013-001 re-raises. The prior disposition explicitly chose "spec wording in an adjacent clarifying paragraph" as the fix — the current finding's objection is that this choice of *location* (adjacent paragraph vs. inline row text) is insufficiently "folded back," not that the mechanism is missing or wrong. That is a formatting preference, not a newly discovered defect.

4. **The proposed mitigation confirms the finding's own churn classification.** The finder's own "Mitigation" text asks only to "fold the grandfather-baseline exemption into L-1's own row definition... Text-only fix; no new rule." Merging existing, already-complete, already-cross-referenced prose into a table cell changes zero runtime behavior of any implementer who reads the section (rather than only the row in isolation) — which is exactly the "optional polish, already scheduled elsewhere" class the remediation-value lens directs to REFUTE. The package has already absorbed nine remediation iterations narrowly targeting this precise L-1/grandfather/`ADR-150-001` interaction (RT-101/RT-104 iter-6 regex widening, FM-002-iter6 count narrowing, IN-001-iter7 R-13 disclosure, IN-001-iter8 the clarification paragraph itself, RT-001/012-003-iter9 the two-clause scan and ratification anchor); a tenth pass asking only to relocate already-existing, already-correct text inside the same section does not change any real adoption or CI-build outcome.

5. **No implementation-failure risk survives the full-section read.** The finder's "Consequence" claims an implementer following "either document's L-1 row" literally would find the mandatory regression test cannot go green "without an undocumented ad-hoc fix invented at build time." This overstates the isolation of the row: the fix (ratification-baseline exemption) *is* documented, in the same subsection, referenced by name from the grandfather-test paragraph's own cross-reference chain. There is no undocumented ad-hoc step required — the baseline-list construction and its exemption semantics are spelled out in enough operational detail (data list, ratification date, exemption test) that an implementer has everything needed to write the L-1 check correctly on first pass.

**Conclusion:** 013-001 identifies a genuine textual style choice (exemption stated in adjacent prose rather than inlined into a table cell) but not a genuine specification gap or implementation-blocking contradiction. Under the remediation-value lens, fixing it changes no adoption outcome and duplicates content already present and already cross-referenced twice over (table header + IN-001-iter8 paragraph). **REFUTED.**

---

## Summary for Structured Output

- Lens: remediation-value
- Verified Critical IDs: none
- Refuted Critical IDs: 013-001
- Note: 013-002 (Major) is out of scope for this Critical-only panel and was not adjudicated.
