# S-010 Self-Refine — Findings (Iteration 10)

> Strategy: S-010 Self-Refine (Madaan et al. 2023) · Owner/creator: ps-architect · Cognitive mode: convergent
> Deliverables reviewed: `ADR-PROJ031-004-adr-identifier-convention.md` (top changelog **v1.11**) + `adr-standards-rule-draft.md`
> Verified-against register: `orchestration/adr-convention-20260702-001/subtraction-pass-notes.md` (residual register R-1…R-17, R-A/R-B/R-C)
> Doctrine: subtraction (no new machinery; 5-rule lint core stays 5). P-002 incremental. P-020 in-mandate. P-022 file+line evidence; inference labeled.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy/deliverable/criticality metadata |
| [Summary](#summary) | Overall assessment |
| [Verification Ledger](#verification-ledger) | Task-specified checks, each PASS/observation |
| [Findings Table](#findings-table) | All findings, severity-sorted |
| [Finding Details](#finding-details) | Expanded Minor findings |
| [Scoring Impact](#scoring-impact) | Findings mapped to the 6 dimensions |
| [Decision](#decision) | Outcome, rationale, next action |

---

## Header

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | ADR-PROJ031-004 (ADR identifier/location/promotion convention) + companion rule draft |
| Criticality | C4 (framework-wide governance; AE-002/AE-003 set a C3 floor, C4 by tier definition) |
| Date | 2026-07-06 |
| Reviewer | ps-architect (creator/owner) |
| Iteration | 10 of the adversary corpus (this is the post-iteration-9 self-refine pass) |
| Objectivity check | High prior investment (9 prior iterations) → leniency-bias counteraction applied per Step 2; forced ≥3 findings on a package that verifies clean |

---

## Summary

The package is **internally consistent and every task-specified verification item PASSES.** The four load-bearing D-4 counts (16 whole dialect corpus / 15 dialect-reachable / 3 canonical / 18 regression) were **independently re-verified against the live filesystem** and match exactly, with the two-clause pre-flight scan reaching 18 files and `sort | uniq -d` empty (no collision). R-14…R-17 are defined in the ADR Risks register and cross-referenced per their iteration-8 disposition homes; the L-1 grandfather clause is present in both files and correctly re-anchored to ratification time (012-003-iter9); nav tables cover all 25 h2 sections; there are **zero dangling in-page anchors** and no ambiguous duplicate anchors in either file; all cross-file relative links resolve; token figures are honest (measured 253 lines / 4111 words / ~5549 tokens, exactly as claimed).

**No Critical and no Major findings.** Three **Minor** findings surface, two of which live only in the `subtraction-pass-notes.md` register (a process/disposition file, not a graded deliverable) and are already reconciled by that same file's downstream sections; the third is a cosmetic cross-reference-parity nit inside the ADR that matches the iteration-8 disposition by design. No edits are made: the two deliverables need none (P-020 scopes edits to deliverables, which pass), and the subtraction doctrine plus iteration-10 maturity argue against churn.

**Version note (not a deliverable defect):** the invoking task labels the package "v1.10," but both deliverables are actually at **v1.11** — the iteration-9 remediation (RT-001 two-clause scan, RT-002 topology substitution, 012-003 ratification-anchor) was appended as v1.11 to both changelogs. All the v1.10 fix-pass items the task asks to verify (D-4, R-14…R-17, L-1 grandfather, honest token figures) are present *and* carried forward correctly through v1.11. The label lag is in the task framing, not the artifact; the artifact's 1.10→1.11 sequencing is honest and monotonic.

---

## Verification Ledger

| # | Task-specified check | Result | Evidence |
|---|----------------------|--------|----------|
| V-1 | D-4 count reconciliation (16/15/3/18) | **PASS — filesystem-verified** | `find docs/design -maxdepth 1 -name 'ADR-*.md'` = **3**; `find projects -path '*/decisions/*' -name 'ADR-*.md'` = **15**; whole dialect corpus (`ADR-{PROJ\|EPIC\|FEAT\|STORY}NNN` + `ADR-150` anywhere) = **16**; two-clause scan reached = **18**; `ADR-STORY015-001` present, entity-embedded, out-of-scan (in `PROJ-024.../STORY-015.../`) |
| V-2 | Two-clause pre-flight scan reaches 18 and `uniq -d` empty | **PASS** | Ran ADR L1 command (lines 407-413) + rule-draft command (lines 188-194): reached 18, `sort\|uniq -d` returned empty (no collision) |
| V-3 | R-14 anchored | **PASS (per iter-8 disposition)** | Defined ADR Risks row (line 478 → `#risks` resolves); referenced rule-draft §Frozen-and-Grandfathered (line 94) + changelog v1.10 (line 788). No in-ADR-body `(#risks)` pointer — matches disposition "ADR §Risks R-14; rule-draft §Frozen" (see SR-003) |
| V-4 | R-15 anchored | **PASS (per iter-8 disposition)** | Defined ADR Risks row (line 479); referenced rule-draft ADR-M-001 (line 46). Guidance root-cause closed at ADR-M-001 |
| V-5 | R-16 anchored | **PASS** | Defined ADR Risks row (line 480); in-body `[R-16](#risks)` at L-7 row (line 690); rule-draft L-7 row (line 179) |
| V-6 | R-17 anchored | **PASS** | Defined ADR Risks row (line 481); in-body `[R-17](#risks)` at Amend-vs-Supersede (line 618); rule-draft §Supersede-and-Amend (line 151) |
| V-7 | L-1 grandfather clause | **PASS** | ADR lines 692-693 ("How pre-adoption grandfathered is operationalized on a subsequent edit"); rule-draft line 183. Both anchor the baseline to **ratification time (2026-07-05/06)**, not lint-ship (012-003-iter9). No sixth rule; core stays L-1/L-2/L-3/L-4/L-7 |
| V-8 | Honest token figures | **PASS** | `wc`: rule-draft = **253 lines / 4111 words / ~5549 tokens (×1.35)** — matches the claim "~5.5k tokens / 253 lines / ~4.1k words" in rule-draft L5 Notes (line 208), rule-draft changelog v1.11 (line 251), and subtraction-notes Files Edited (line 233). Single current figure, reconciled across all three primary sources |
| V-9 | Nav tables cover all `##` sections | **PASS** | ADR: 25 h2 sections, all 25 in nav table; rule-draft: nav table complete |
| V-10 | No dangling refs | **PASS** | GitHub-accurate slug check: ADR 108 in-page link occurrences / 34 distinct targets → **0 dangling, 0 ambiguous**; rule-draft 18 occurrences / 14 targets → **0 dangling, 0 ambiguous**. The 4 double-hyphen anchors (em-dash headings) resolve correctly |
| V-11 | Cross-file relative links resolve | **PASS** | `../FEEDBACK-LOG.md`, `../design/adr-standards-rule-draft.md`, `ADR-PROJ031-003-*.md`, `../orchestration/.../subtraction-pass-notes.md` all exist; `#claim-status-convention-p-022--foundational` matches the h2 in ADR-PROJ031-003 (line 73) |
| V-12 | Overclaimed coverage (Critical) vs disclosed-residual (valid MEDIUM) | **PASS** | Every uncovered gap is labeled `[INHERENT]`/`[DISCLOSED]`/`[DELETION-INHERENT]`/`[DESIGN-INHERENT]` with a named home in R-1…R-17 / R-A/R-B/R-C. No mechanism is asserted as achieved that the 5-rule core does not deliver; lint is consistently "designed-not-built (Claim-Status)" |

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SR-001-20260706 | subtraction-notes "Budgets Achieved" table + honest-note present **~3,248 tokens / 233 lines** as the "After" achieved state; the rule-draft has since grown to **253 lines / ~5.5k tokens** (documented in the same file's Files Edited row + iter-8/9 sections) without a currency qualifier in the Budgets section | Minor | `subtraction-pass-notes.md:71-75` ("After ~3,248 / 233") vs `:233` ("253 lines / ~5.5k tokens … the single current figure") | Internal Consistency |
| SR-002-20260706 | subtraction-notes document **title** reads "(Iteration 5 → 6 remediation)" but the file now spans iterations 5-9 (carries Iteration-8 and Iteration-9 remediation sections) — stale scope parenthetical | Minor | `subtraction-pass-notes.md:1` vs `:181` (Iteration-8) and `:207` (Iteration-9) | Internal Consistency |
| SR-003-20260706 | Cross-reference-parity nit in the ADR: R-16/R-17 carry in-body `(#risks)` pointers (L-7 row / Amend note), but R-14/R-15 have no in-ADR-body anchored cross-ref — R-14's natural home is the ADR L-2 frozen-dir row. Matches the iteration-8 disposition (which routed R-14→rule-draft §Frozen, R-15→rule-draft ADR-M-001), so **not a broken reference** — a cosmetic traceability asymmetry | Minor | ADR `:687` (L-2 frozen-dir row, no R-14 pointer) vs `:690`/`:618` (R-16/R-17 pointers) | Traceability |

*All three are register-scoped or cosmetic. Zero Critical, zero Major. No finding requires restoring deleted machinery.*

---

## Finding Details

### SR-001-20260706: Budgets-Achieved snapshot is locally stale
- **Severity:** Minor · **Dimension:** Internal Consistency
- **Evidence:** `subtraction-pass-notes.md:71` (`Rule-draft tokens … **~3,248**`), `:72` (`**233**` lines), `:75` (honest-note repeats ~3,248/233); contrast `:233` (`253 lines / ~5.5k tokens … the single current figure`).
- **Impact:** A reader consulting only the "Budgets Achieved" section gets the subtraction-pass snapshot (~3.25k tokens), which the rule-draft has since outgrown (5.5k). The file as a whole remains honest — the growth 233→238→242→247→253 is fully traced in the iter-6/8/9 sections and the Files Edited row — so this is *local* staleness, not deception. The two **graded deliverables** carry the correct 253/~5.5k figure everywhere.
- **Recommendation (optional, non-blocking):** add a one-clause currency pointer to the Budgets honest-note, e.g. "(snapshot at the subtraction pass; grew to 253 lines / ~5.5k tokens by iter-9 — see [Files Edited])". Pure disclosure, no machinery. *Not edited in this pass:* the register is outside the task's deliverable-editing scope (P-020), and the current figure is already authoritative in Files Edited.

### SR-002-20260706: stale document-title scope parenthetical
- **Severity:** Minor · **Dimension:** Internal Consistency
- **Evidence:** `subtraction-pass-notes.md:1` — "(Iteration 5 → 6 remediation)"; the file now contains `## Iteration-8 Remediation` (`:181`) and `## Iteration-9 Remediation` (`:207`).
- **Impact:** Cosmetic — the nav/section index (`:19-20`) already lists the iter-8/iter-9 sections, so a reader is not misled about scope; only the title's parenthetical undersells the file's span.
- **Recommendation (optional, non-blocking):** widen the parenthetical to "(Iterations 5-9 remediation)". *Not edited* — same register/mandate rationale as SR-001.

### SR-003-20260706: R-14/R-15 lack the in-body `(#risks)` pointers R-16/R-17 carry
- **Severity:** Minor · **Dimension:** Traceability
- **Evidence:** ADR `:690` has `[R-16](#risks)` at the L-7 row; `:618` has `[R-17](#risks)` at the Amend-vs-Supersede note. The ADR L-2 row (`:687`, frozen-dir exemption — exactly the R-14 topic) has no `[R-14](#risks)` pointer; R-15 (frontmatter `id:`) has no ADR-body home (there is no ADR-M-001 inside the ADR).
- **Impact:** Minor traceability asymmetry among the four iteration-8 residuals. **Not a defect against the disposition:** the iteration-8 subtraction notes deliberately routed R-14→"rule-draft §Frozen-and-Grandfathered" and R-15→"rule-draft ADR-M-001" (both present and correct), reserving the in-body ADR pointers for R-16/R-17. So the current state is by-design; the four residuals simply are not uniformly cross-linked inside the ADR body.
- **Recommendation (optional, non-blocking):** for full parity, append "([R-14](#risks))" to the ADR L-2 frozen-dir row — a one-token, subtraction-consistent traceability add. *Not edited* — the iteration-8 disposition intentionally chose R-14's home elsewhere; churning it at iteration 10 risks re-opening a settled disposition for negligible gain.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | Every task-specified check has a home; all 6 self-critique dimensions examined; ≥3 findings surfaced under leniency counteraction |
| Internal Consistency | 0.20 | Positive (deliverables) / minor-Negative (register) | Deliverables reconcile across D-4, counts, token figures; SR-001/SR-002 are localized register staleness, downstream-reconciled |
| Methodological Rigor | 0.20 | Positive | Counts independently re-verified against the filesystem (not taken on trust); anchors checked with GitHub-accurate slugging; all 6 S-010 steps executed |
| Evidence Quality | 0.15 | Positive | Every finding and verification carries a file:line reference; false-positive `ADR-150`→"R-15" substring matches identified and excluded |
| Actionability | 0.15 | Positive | Each Minor has a concrete, optional, non-blocking recommendation with a stated no-machinery guarantee |
| Traceability | 0.10 | Neutral | SR-003 notes a cosmetic in-body cross-ref asymmetry; residuals otherwise trace cleanly to R-1…R-17 / R-A/R-B/R-C |

---

## Decision

**Outcome: PASS — ready for external review / gate.** The two deliverables are internally consistent; the disclosed-residual posture (R-1…R-17, R-A/R-B/R-C) is an honest MEDIUM-tier stance, not overclaimed coverage; and all task-specified v1.10 (carried through v1.11) fix-pass items verify — several against the live filesystem.

**Rationale:** Zero Critical, zero Major. The three Minor findings are (a) two localized staleness items in the `subtraction-pass-notes.md` **register** (not a graded deliverable), each already reconciled by that same file's downstream sections; and (b) one cosmetic cross-reference-parity nit inside the ADR that matches the iteration-8 disposition by design. None implicates the 5-rule lint core, none requires restoring deleted machinery, and none affects the correctness of the convention as authored.

**No edits made (P-020, subtraction doctrine):** the task scopes editing to the deliverables, which need none; the register Minors are honesty-improvements available to a future maintenance pass but are outside this pass's edit mandate and are already non-deceptive in situ.

**Next action:** none required for the deliverables. Optionally, a future non-adversarial maintenance pass may apply the three one-clause disclosure recommendations (SR-001/SR-002/SR-003) to the register and the ADR L-2 row — all pure disclosure, no machinery.
