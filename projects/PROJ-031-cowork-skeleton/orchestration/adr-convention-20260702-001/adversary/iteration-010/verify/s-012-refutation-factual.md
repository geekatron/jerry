# S-012 Refutation Panel — FACTUAL Lens (Iteration 10)

## Scope

Target report: `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-012-findings.md`

Only Critical-severity findings are in scope per mandate. The report contains exactly one Critical finding: **012-004**. (012-005 and 012-006 are Major and are out of scope for this panel.)

Protocol: FACTUAL-ACCURACY lens only. Question: does the cited defect actually exist in the CURRENT deliverables at the cited locations? Re-read exact lines; misreadings, stale references, and restatements of already-disclosed residuals (R-1..R-17 or the disposition tables in `subtraction-pass-notes.md`) are REFUTED.

---

## 012-004: Grandfather-baseline enumeration excludes PROJ-014's bare drafts, which L-2's unscoped wording would otherwise catch

**Verdict: VERIFIED**

**Citation check (all confirmed accurate against current file content):**

- ADR line 686 (L-1 row) ends with the literal scope qualifier `projects/*/decisions/`, `docs/design/.` — confirmed verbatim. Rule draft line 175 carries the identical trailing qualifier — confirmed.
- ADR line 687 (L-2 row): `A git-added file must not match ^ADR-\d, except in frozen dirs (docs/adrs/, docs/archive/).` — confirmed verbatim, with **no scan-scope qualifier**, unlike L-1's row. Rule draft line 176 reads `...anywhere except frozen dirs...` — confirmed, "anywhere" is explicit.
- ADR line 517 (Migration Plan): `PROJ-014 bare ADR-001..004 (orchestration artifacts) | Transient, colliding with docs/adrs/ | Low priority; rename to a domain slug (or ADR-PROJ014-NNN dialect) only if promoted into a decisions/ home | Low` — confirmed verbatim.
- Rule draft line 94 (Frozen and Grandfathered Legacy): `**PROJ-014's bare ADR-001..004 are transient bare drafts** (deprecated Scheme-E numbering, not a recognized dialect) — grandfathered only as historical artifacts, to be re-slugged if ever promoted.` — confirmed verbatim.
- ADR line 393 (Canonical Location Model, Orchestration drafts row): classifies `projects/*/orchestration/.../` as **Transient (non-canonical)** — confirmed, and this is PROJ-014's location class, distinct from **Frozen** (`docs/adrs/`, `docs/archive/`), the only class L-2's exemption clause names.
- ADR lines 225-231 (D-4 grandfather-count reconciliation) and ADR line 693 / rule draft line 183 (ratification-time baseline mechanism): confirmed the operational baseline is defined precisely and only as "the 18 reachable [15 dialect-reachable + 3 canonical] ... plus the out-of-scan `ADR-STORY015-001`" — i.e., 19 named items. Verified this exact 19-item enumeration nowhere includes PROJ-014's 4 bare files; the 16-item "whole dialect corpus" (`EPIC002×2, PROJ010×6, PROJ022×2, PROJ031×4, STORY015×1, 150×1 = 16`, ADR line 226) also excludes them by construction, since PROJ-014's files are bare (`ADR-NNN`), not dialect-form (`ADR-PROJ014-NNN`).

**Analysis of the substantive claim:**

The technical claim is factually accurate on direct re-reading: PROJ-014's 4 bare files (a) are in a **Transient**, non-Frozen location, so L-2's own "except in frozen dirs" exemption clause does not reach them; (b) are absent from the 16-item dialect corpus, the 18-item reachable set, and the 19-item ratification-time baseline that ADR line 693 / rule draft line 183 define as *the specific enumerable mechanism* used to decide whether a git-modified file is "grandfathered-exempt from L-1/L-2" versus "held ... as 'new'"; and (c) are separately described in prose (rule draft line 94) as "grandfathered only as historical artifacts" — a claim that the specific operational baseline mechanism does not actually implement, since that mechanism's own enumeration (19 items) omits them. This is a genuine internal inconsistency between a general prose disclosure and the specific, later-defined operational mechanism (introduced in the iter-8/iter-9 passes per 012-003's disposition), not a misreading of either passage.

**Residual/disposition-table check:** Checked against all of R-1 through R-17, R-A/B/C, and PM-009 in `subtraction-pass-notes.md` — none names this specific gap. R-10 (out-of-scan location class) covers entity-embedded and repository-based-topology homes, not PROJ-014's transient orchestration-directory location. R-14 (frozen-dir new-file collision) covers files added *inside* a frozen dir, not PROJ-014's transient, non-frozen location. FM-004 (iteration-6 disposition, `subtraction-pass-notes.md:171,248`) is the closest related item — it produced the current rule-draft line 94 text by "separating" PROJ-014's bare drafts from the grandfathered-dialect corpus — but FM-004's disposition addressed a *counting* miscategorization (PROJ-014 wrongly folded into the dialect-corpus count), not the *operational baseline-enumeration* mechanism that was introduced later (iteration-8/9, via IN-001-iter8 and 012-003-iter9) and that this finding specifically targets. The specific defect named in 012-004 (the 19-item ratification-baseline enumeration silently omitting PROJ-014, contradicting the general "grandfathered ... as historical artifacts" prose) postdates and is distinct from FM-004's fix, and is not named anywhere in the residual register. This finding is therefore not a restatement of an already-disclosed residual.

**Conclusion:** The cited defect exists as described, all citations are accurate, and the gap is not covered by any prior disposition or named residual. **VERIFIED.**

---

## Summary

| ID | Severity | Verdict |
|----|----------|---------|
| 012-004 | Critical | VERIFIED |

(012-005, 012-006: Major, out of scope for this Critical-only refutation panel.)
