# FMEA Report: ADR-PROJ031-004 + adr-standards-rule-draft.md (Post-Subtraction Package, Iteration 7)

**Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-012 FMEA, blind reviewer, iteration 7)
**H-16 Compliance:** S-003 Steelman embedded per-option in the ADR's `Options Considered (A-F)` section, per the ADR's own self-declaration (lines 65-68). This reviewer operated under the blind protocol (no access to other adversary-iteration outputs) and did not independently re-verify a discrete, separately-filed S-003 artifact; the embedded-steelman evidence is the verifiable basis.
**Elements Analyzed:** 18
**Failure Modes Identified:** 6
**Total RPN:** 1274

**Scope note (P-020/P-022).** This FMEA evaluates the package **as it now stands after the user-authorized subtraction pass** (FU.1) and the iteration-6 overclaim-correction pass. Per the invoking instruction, no finding below re-demands machinery that was deliberately deleted (the 18-rule lint, the waiver ledger, the two-tier ratification gate, CODEOWNERS-dependent claims). All findings target either (a) internal contradictions in the **retained** content, (b) spec-level gaps in the **retained** 5-rule lint that are independent of the deleted machinery, or (c) a completeness gap in a lifecycle phase (onboarding) explicitly named in the invoking task. Several previously-disclosed residuals (R-1 through R-11, R-A/R-B/R-C, PM-009) were reviewed and found to be **honestly and adequately framed on their own merits** — these are noted in the Summary rather than re-raised as findings.

---

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall FMEA assessment |
| [Element Inventory](#element-inventory) | MECE decomposition of the lifecycle |
| [Findings Table](#findings-table) | All FM-NNN findings with RPN |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Disclosed-Residual Posture Assessed on Its Merits](#disclosed-residual-posture-assessed-on-its-merits) | Residuals reviewed and found adequate (not re-raised) |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

18 lifecycle elements analyzed across creation, cross-ref, amend, supersede, promote, the 5-rule lint, and onboarding. 6 failure modes found: **2 Critical** (both internal-consistency contradictions in retained, non-deleted content — a Status Vocabulary self-contradiction on whether `DEPRECATED` is truly terminal, and a grandfather-regression-test file-count contradiction that the changelog claims was already fixed but was not fully propagated) and **4 Major** (an L-4 lint-rule spec gap omitting the `FEAT` dialect prefix, a genuine onboarding-narrative gap left by the subtraction pass, an amplification of the already-disclosed R-11 lint asymmetry with a concrete Supersede-lifecycle consequence, and a cost-label inconsistency for this ADR's own self-promotion). None of the findings ask to restore deleted enforcement machinery; all are either logic contradictions within retained prose or narrow spec-completeness gaps in the retained 5-rule core. **Recommendation: REVISE (targeted).** The two Criticals are single-paragraph/single-cell corrections, not architectural rework, and are consistent with the subtraction doctrine (fix the exposing claim, add nothing).

---

## Element Inventory

| # | Element | Lifecycle Phase | Description |
|---|---------|------------------|-------------|
| E1 | ID Grammar (canonical + dialect regex) | Creation | `ADR-M-001..006`; canonical/dialect/deprecated/frozen regex definitions |
| E2 | Location assignment (topology-aware) | Creation | Canonical Location Model; project-based vs. repository-based `ONE-OF` |
| E3 | Frontmatter schema (YAML `---` block) | Creation | `id/type/status/scope/origin_project/...`; dual YAML+blockquote coexistence |
| E4 | Citation handling (bare-ID vs. full-path) | Cross-ref | Path-1 zero-churn claim; R-B residual (full-path/GH-Issue staleness) |
| E5 | Structural relationship resolution | Cross-ref | L-7 existence-only check; R-11 3-of-6 field asymmetry |
| E6 | In-body amendment mechanism | Amend | `**AMENDED YYYY-MM-DD:**` block; amendment-boundary (scope/origin/location frozen) |
| E7 | Amendment mutation detection | Amend | R-C residual (in-place frontmatter mutation undetectable) |
| E8 | Status Vocabulary and transitions | Amend/Supersede | `PROPOSED/ACCEPTED/REJECTED/DEPRECATED/SUPERSEDED`; valid-transition table |
| E9 | New-ADR supersession mechanism | Supersede | Tombstone, bidirectional back-link, FM-011 cycle residual |
| E10 | Path 0 (draft -> canonical home) | Promote | Graduation of transient/orchestration drafts |
| E11 | Path 1 (canonical, pure `git mv`) | Promote | Zero ID-churn promotion; AE-004 C3-floor scoping |
| E12 | Path 2 (dialect -> canonical, rename+tombstone) | Promote | Discouraged path; AE-004 auto-C4 scoping |
| E13 | L-1 Grammar rule | 5-rule Lint | Canonical-OR-dialect filename match |
| E14 | L-2 No-new-bare rule | 5-rule Lint | Rejects new `^ADR-\d` outside frozen dirs |
| E15 | L-3 No-duplicate-ID rule | 5-rule Lint | `sort \| uniq -d` over canonical+dialect IDs; iter-6 case-class widening |
| E16 | L-4 ID<->location rule | 5-rule Lint | Dialect-prefix-to-directory consistency check |
| E17 | Grandfather regression test | 5-rule Lint | Pre-ship gate; 15/16/18/19-file scan-path corpus counts |
| E18 | Onboarding narrative | Onboarding | Author-facing "how do I create my first ADR" guidance; M-14 scaffold dependency |

---

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|-------------------|--------------------|
| FM-001-20260706I7 | E8 (Status Vocabulary) | `DEPRECATED` is declared terminal ("do not transition further") in two places, yet a third passage in the same section prescribes `DEPRECATED` -> `SUPERSEDED` as "the correct handling" | 7 | 8 | 7 | 392 | Critical | Add a `DEPRECATED`\|`SUPERSEDED` row to the valid-transitions table; qualify the "do not transition further" sentence with "except DEPRECATED->SUPERSEDED, per the forward-link asymmetry note below" | Internal Consistency |
| FM-002-20260706I7 | E17 (Grandfather test) | Migration-Plan row M-6 states the grandfather test covers "16 dialect + 3 canonical = 19 files pass L-1," directly contradicting the Enforcement Design section and the rule draft (both: 18 files reachable, STORY015 explicitly out-of-scan/untested) — a defect the changelog (v1.8) claims was already fixed but was not propagated to the M-6 row | 6 | 8 | 7 | 336 | Critical | Edit the M-6 row's parenthetical to "15 dialect + 3 canonical = 18 files reachable by the scan path pass L-1 (STORY015 out-of-scan, R-10)" | Internal Consistency |
| FM-003-20260706I7 | E16 (L-4 rule) | L-4's own rule description, in both deliverables, enumerates only `PROJ{NNN}`/`EPIC{NNN}`/`STORY{NNN}` as checked dialect prefixes, omitting `FEAT` — even though `FEAT` is the 4th member of the closed dialect-prefix set the grammar and Location Model both define | 6 | 3 | 7 | 126 | Major | Add `FEAT{NNN}` to L-4's rule-description prose in both files (one-line addition; no new mechanism) | Methodological Rigor |
| FM-004-20260706I7 | E18 (Onboarding) | No consolidated author-facing onboarding narrative survives the subtraction pass; guidance is scattered across 5+ sections, and M-14 (documenting `decisions/` in the worktracker scaffold SSOT) is still an open TBD-Task, so a new-project author following only the scaffold docs would not learn a `decisions/` directory is expected | 5 | 6 | 5 | 150 | Major | Add a short (10-15 line) "Authoring your first ADR" checklist pointing to the existing ID Scheme / Frontmatter Schema / Location Model sections rather than restoring the deleted section's prose | Completeness |
| FM-005-20260706I7 | E9 (Supersession mechanism) | The disclosed R-11 asymmetry (only `superseded_by`/`promoted_to`/`promoted_from` are lint-checked) has a concrete, not-yet-drawn-out consequence: a new ADR can declare `supersedes: [old-id]` while the "superseded" predecessor's own `status`/`superseded_by` fields are never touched or lint-verified, so the predecessor can silently keep reading `ACCEPTED` with no forward pointer | 6 | 5 | 6 | 180 | Major | Add one sentence to R-11's disclosure naming this specific consequence (a still-`ACCEPTED`-looking superseded predecessor) as an author-facing SHOULD-check at supersession time; no new lint rule | Traceability |
| FM-006-20260706I7 | E12 (Path 2 / this ADR's own promotion) | The corpus-state Migration-Plan table labels this ADR's own Path-2 self-promotion (M-9) cost as "Trivial," while the ordered action-items table's own M-9 entry describes a multi-part, atomicity-constrained, not-yet-instrumented operation | 3 | 5 | 6 | 90 | Major | Change the corpus-state table's cost cell from "Trivial" to "Low (coordinated with M-2; see M-9 action item)" | Actionability |

**Finding ID Format:** `FM-{NNN}-20260706I7` (iteration 7, 2026-07-06).

---

## Finding Details

### FM-001-20260706I7: Status Vocabulary self-contradiction on `DEPRECATED` terminality

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR `## Status Vocabulary` |
| **Strategy Step** | Step 2 (Enumerate) / Step 3 (Rate) — Inconsistent lens |

**Evidence:**
- `ADR-PROJ031-004-adr-identifier-convention.md:620`: "Terminal states (`SUPERSEDED`, `DEPRECATED`) do not transition further — a superseded decision that becomes relevant again is addressed by a *new* ADR, never by reviving the old status (Nygard immutability)."
- `ADR-PROJ031-004-adr-identifier-convention.md:592`: "...The [Status Vocabulary](#status-vocabulary) states terminal states 'do not transition further,' but that rests on SHOULD-NOT discipline, not a lint check..." (reinforces the terminal framing as settled).
- `ADR-PROJ031-004-adr-identifier-convention.md:622`: "**On the DEPRECATED/SUPERSEDED forward-link asymmetry (FM-107...).** ... The correct handling if a DEPRECATED decision *does* later acquire a specific replacement is to use the **SUPERSEDED** relationship (which already carries the bidirectional link and L-7 check), not to bolt a forward-link onto DEPRECATED."

**Analysis:** Line 620 (reinforced at line 592) asserts `DEPRECATED` cannot transition further — it is terminal, full stop. Line 622, in the very same document section, describes a scenario in which a `DEPRECATED` ADR *does* transition to `SUPERSEDED` and calls this "the correct handling." These two statements cannot both be true as written: either `DEPRECATED` is terminal (no valid outbound transition, contradicting 622's prescription) or `DEPRECATED -> SUPERSEDED` is a valid transition (contradicting 620's "do not transition further" and the missing row in the Valid Status Transitions table, which lists only `PROPOSED->ACCEPTED`, `PROPOSED->REJECTED`, `ACCEPTED->SUPERSEDED`, `ACCEPTED->DEPRECATED`, `REJECTED->PROPOSED`). This is a pure Internal Consistency defect in retained, non-deleted content — unrelated to the subtraction doctrine — and it sits in the Status Vocabulary section that governs both the Amend and Supersede lifecycle phases the invoking task named explicitly. Eight prior adversarial iterations did not catch this specific contradiction (FM-107 itself, which introduces the contradiction, is tagged iter-3 and was never reconciled against the transition table added independently).

**Corrective Action:** Add a `DEPRECATED` -> `SUPERSEDED` row to the Valid Status Transitions table with trigger "A specific replacement is later identified for a previously-unreplaced deprecation (see FM-107 asymmetry note)"; soften line 620's "do not transition further" to "do not transition further, except that a `DEPRECATED` ADR may later be re-classified `SUPERSEDED` if a specific replacement is identified (see below)." This is a two-cell/one-clause edit, not new machinery.

**Acceptance Criteria:** The transition table and the two prose passages (620, 622) describe the identical rule with no contradiction.

**Post-Correction RPN estimate:** ~40 (S=5 residual mild ambiguity risk, O=2, D=4).

---

### FM-002-20260706I7: Grandfather regression-test file-count contradiction (19 vs. 18)

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR `## Migration Plan` (M-6 row) vs. `## Enforcement Design (L5 CI Lint)` |
| **Strategy Step** | Step 2 (Enumerate) — Inconsistent lens |

**Evidence:**
- `ADR-PROJ031-004-adr-identifier-convention.md:517` (Migration Plan, M-6 row): "...with the grandfather regression test green (**16 dialect + 3 canonical = 19 files pass L-1**) plus one named red-then-green fixture per rule."
- `ADR-PROJ031-004-adr-identifier-convention.md:664` (Enforcement Design section): "A grandfather regression test gates the lint before it ships: the **18 files reachable by the scan path** (15 dialect files in `decisions/` dirs + 3 canonical `docs/design/` ADRs) pass L-1... The entity-embedded `ADR-STORY015-001` (no `decisions/` in its path) is **out-of-scan** (R-10, FM-002), grandfathered in place but not lint-covered."
- `design/adr-standards-rule-draft.md:94`: "Of the 16-file dialect corpus + 3 canonical ADRs, the **18 reachable** by the `projects/*/decisions/` + `docs/design/` scan path pass the grandfather regression test; the entity-embedded `ADR-STORY015-001` is out-of-scan (R-10)."
- `ADR-PROJ031-004-adr-identifier-convention.md:753` (Changelog v1.8): "...**EDIT/NARROW:** grandfather test **19->18 reachable**, STORY015 disclosed out-of-scan R-10 (FM-002)..." — this changelog entry explicitly claims the 19-to-18 correction was already made.

**Analysis:** Three of four locations (Enforcement Design, rule draft, and the changelog's own description of the fix) agree the grandfather test reaches only **18** files, with `ADR-STORY015-001` explicitly excluded because it lives outside the `decisions/` scan path (a disclosed residual, R-10). The fourth location — the Migration Plan's M-6 action-item row, which is the row an implementer would actually read when building the lint (M-6) — still says **19** files "pass L-1," which both double-counts the out-of-scan file and asserts it "passes" a check the rest of the document says it never undergoes (out-of-scan means untested, not passing). This is exactly the class of disposition-completeness gap the iteration-6 remediation pass targeted (per its own changelog description at line 753), but the fix was not propagated to all four occurrences. This is a live, currently-present contradiction in retained content, independent of the deleted machinery.

**Corrective Action:** Edit line 517 to read "15 dialect + 3 canonical = 18 files reachable by the scan path pass L-1 (STORY015 out-of-scan, R-10)" to match lines 664 and the rule draft.

**Acceptance Criteria:** `grep -n "19 files\|= 19\|16 dialect + 3 canonical"` over both deliverables returns zero remaining occurrences of the stale "19" figure.

**Post-Correction RPN estimate:** ~30 (S=4, O=2, D=4) — a one-line factual correction with no residual ambiguity once fixed.

---

## Disclosed-Residual Posture Assessed on Its Merits

Per the invoking instruction, the following previously-disclosed residuals were reviewed against the current package and judged **adequately and honestly framed** — no further finding is raised against them:

| Residual | Assessment |
|---|---|
| R-1 (lint may never be built) | Honestly framed as a decoupled, non-blocking enhancement; guidance value is not contingent on it. Adequate. |
| R-6 (cross-branch same-slug race) | Detection path (L-3 CI + pre-flight one-liner, both verified via Grep to use the corrected `[A-Za-z0-9-]` class in all 4 ADR occurrences) is concrete and monitored (PM-009 threshold: >=2 collisions/90-day window). Adequate. |
| R-7 (slug reuse for unrelated subject) | Named, unmitigated-by-lint, with a named escalation path (per-slug-family review). Adequate for a MEDIUM-tier convention. |
| R-9 (case-fold look-alike) | Correctly downgraded from an earlier over-claim to SHOULD-NOT guidance; the residual is real but proportionate to a MEDIUM-tier, solo-maintainer context. Adequate. |
| R-B (citation staleness, incl. GitHub Issues) | Bounded honestly: Path-1's ID-stability removes churn for the ~72% bare-ID majority; the ~28% full-path minority is disclosed with a named manual-sweep fallback and an owner+cadence (governance, at each promotion). Adequate. |
| R-C (in-place amendment mutation undetectable) | Correctly labeled [INHERENT] — no lint can see a mutation that moves nothing and renames nothing. Adequate. |

This confirms the subtraction pass's central claim — that closing findings by deletion rather than compensating machinery is sound — largely holds for the enforcement-scope residuals. The findings in this report are a different class: internal-consistency defects and narrow spec gaps in the **retained** content that the subtraction/remediation doctrine did not (by its own design) go looking for, since its focus was overclaim and machinery-growth, not cross-section arithmetic/logic reconciliation.

---

## Recommendations

Ordered by RPN (highest first):

1. **FM-001 (RPN 392, Critical).** Add the missing `DEPRECATED -> SUPERSEDED` transition row and soften the "do not transition further" absolute at line 620. Estimated effort: one table row + one clause edit.
2. **FM-002 (RPN 336, Critical).** Correct the M-6 row's file count from 19 to 18 (line 517) to match the already-corrected Enforcement Design section, rule draft, and the changelog's own claim of having made this fix. Estimated effort: one sentence edit.
3. **FM-005 (RPN 180, Major).** Add one sentence to the R-11 disclosure naming the "stale-`ACCEPTED`-predecessor" consequence explicitly.
4. **FM-004 (RPN 150, Major).** Add a compact "Authoring your first ADR" pointer-checklist (not a restoration of the deleted section's prose) cross-referencing existing sections.
5. **FM-003 (RPN 126, Major).** Add `FEAT{NNN}` to L-4's rule-description prose in both files.
6. **FM-006 (RPN 90, Major).** Recalibrate the M-9 cost-estimate cell from "Trivial" to "Low (coordinated with M-2)".

None of the six corrective actions restores deleted enforcement machinery; all are narrow prose/table edits within the doctrine the subtraction pass itself established (fix the exposing claim, add nothing).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-004: onboarding narrative gap for new authors |
| Internal Consistency | 0.20 | Negative | FM-001 and FM-002: two live self-contradictions in retained content (Status Vocabulary; grandfather-test file count) |
| Methodological Rigor | 0.20 | Negative | FM-003: L-4 lint-rule spec omits a member of its own closed dialect-prefix set |
| Evidence Quality | 0.15 | Neutral | All findings in this report are grep-verified against exact line numbers in both deliverables; no fabricated claims |
| Actionability | 0.15 | Negative | FM-006: cost-estimate inconsistency slightly undermines the Migration Plan's Actionability, though all 6 corrective actions here are themselves highly concrete |
| Traceability | 0.10 | Negative | FM-005: the disclosed R-11 residual does not yet trace to its specific downstream consequence for the Supersede lifecycle |

---

## Execution Statistics
- **Total Findings:** 6
- **Critical:** 2
- **Major:** 4
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5
