# Owner-First Remediation Notes — Iteration 3

> **Owner:** ps-architect (creator/owner of the ADR convention)
> **Deliverables edited:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`, `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
> **Input:** `adversary/iteration-003/s-014-quality-score.md` (Priority-Ordered Remediation Table) + all 9 blind-strategy findings files
> **Score being remediated:** 0.62 (engagement gate 0.95; SSOT gate 0.92) — REJECTED
> **Method:** Every [FIXABLE-NOW] item edited directly; [INHERENT] items given honest Claim-Status framing; invalid items rebutted with cited evidence (P-022). All factual claims below are grep/ls-verified against the live repo on 2026-07-02.

## Navigation

| Section | Purpose |
|---------|---------|
| [Empirical Verifications](#empirical-verifications) | Load-bearing facts checked before editing |
| [Disposition Log](#disposition-log) | Per-priority-item outcome (FIXED / REBUTTED / FRAMED) |
| [Rebuttals](#rebuttals) | Items judged invalid or mis-scoped, with evidence |
| [Tally](#tally) | Counts |

---

## Empirical Verifications

All verified 2026-07-02 against the live worktree (P-022; commands are reproducible):

| # | Claim under test | Command result | Bearing |
|---|------------------|----------------|---------|
| V-1 | `.claude/rules/` symlink granularity (PM-101) | `.claude/rules -> ../.context/rules` is a **directory-level** symlink; files inside are plain files exposed through it. | M-2b's "create a per-file symlink" step is STALE — adding `.context/rules/adr-standards.md` auto-exposes it. Corrected. |
| V-2 | CODEOWNERS ownership (PM-102) | Every governed path (`.context/rules/`, `.github/workflows/`, `docs/governance/`) is owned by the single identity `@geekatron`. | The "distinct second-reviewer with review authority" waiver is currently unsatisfiable. Disclosed + solo-maintainer fallback added. |
| V-3 | ps-architect.md grammar footprint (CV-001) | Non-canonical filename grammar `{ps_id}-{entry_id}-adr-*.md` on lines 260, 268, 497, 500, 503, 506 (**6 lines**); non-compliant title `ADR-{NUMBER}` on line 218 (**1**); phantom `python3 scripts/cli.py` on 267, 509 (**2**). | The "~6 vs 10" scalar fight is methodology-dependent; replaced with the grep breakdown in both files. |
| V-4 | Bare-ID vs full-path ADR citation ratio in `.context/rules/` (DA-001) | **28 bare-ID** citations vs **11 full-path** citations (~72% : ~28%). | Bare-ID *dominates* the SSOT corpus — the ADR's "overwhelming majority bare-ID" claim is substantiated, but full-path is a real ~28% minority (not "a single ci.yml example"). Claim re-scoped with the measured ratio. |
| V-5 | Repository-based worktracker topology (FM-102) | SSOT documents both `Project-based (ONE-OF)` and `Repository-based (ONE-OF)`; repository-based uses `{RepositoryRoot}/work/`, no `projects/` prefix. | Convention had no repository-based location row. Added + onboarding/lint branched on topology. |
| V-6 | `jerry ast frontmatter` parser (CC-003) | `jerry ast frontmatter <file>` extracts **blockquote** frontmatter ("Extract all blockquote frontmatter fields", `skills/ast/SKILL.md:105`), NOT YAML `---`. | Mandated YAML `---` frontmatter needs a parser the `ast` tool does not provide; reconciliation added + YAML parsing scoped into M-6. |
| V-7 | EPIC002 collision resolution (CV-002) | `ADR-EPIC002-001-strategy-selection.md` and `ADR-EPIC002-002-enforcement-architecture.md` both exist in `PROJ-001-oss-release/decisions/`; `ADR-output-path-resolution-001.md` is in `docs/design/`. | The output-path decision (born `ADR-EPIC002-001`) was resolved by renaming to `ADR-output-path-resolution-001`, NOT to `ADR-EPIC002-002`. Context section corrected. |

---

## Disposition Log

| Prio | ID(s) | Disposition | What changed / where |
|------|-------|-------------|----------------------|
| 1 | IN-001 | **FIXED** | Added a **Ratification Gate** H3 under `## Status` with 4 falsifiable pre-conditions (G-1..G-4) that a reviewer/CI can check true/false; applies the doc's own "prose row is not evidence" principle to its own `PROPOSED→ACCEPTED` flip. ADR only. |
| 2 | CC-002 | **FIXED** | L-9 reworded `non-waivable-in-practice` → `waivable-in-principle; see tier reconciliation` in **both** files, matching the CC-001 fix already applied to L-2/L-3. |
| 3 | RT-002 | **FIXED (spec)** | L-10 rescoped from `docs/design/README.md` framework-registry-only → **repo-wide canonical slugs (framework + every `projects/*/decisions/`)** in both files; M-5b arbiter rescoped likewise. Actual fuzzy-match tool build remains [INHERENT] pending M-6. |
| 4 | DA-002 | **FIXED** | M-2 and M-9 each gained explicit reciprocal cross-link-repair actions; the ADR↔rule-draft relative links must be re-pointed in the same commit as each move. ADR only (the migration plan lives there). |
| 5 | FM-102 | **FIXED** | Added a **Repository-based `{RepositoryRoot}/decisions/`** row to the Canonical Location Model in both files + a topology-branch note; L-4 lint scoped "project-based topology only, skipped under repository-based"; onboarding step 1 branched on topology. Verified V-5. |
| 6 | CV-002 | **FIXED** | Context section corrected: collision resolved by rename to `ADR-output-path-resolution-001` (NOT `ADR-EPIC002-002`, a separate live ADR). Verified V-7. |
| 6 | CV-001 | **FIXED (breakdown, scalar retired)** | Replaced the "~6 vs 10" scalar dispute with the grep-pinned line-by-line footprint in both files (V-3). Honest conclusion: templated filename grammar on 6 lines; full non-compliant footprint 11 distinct lines. Neither prior scalar was complete. |
| 7 | DA-001 | **FIXED (re-scoped) + partial REBUTTAL** | Added grep-measured ratio **28 bare-ID : 11 full-path (~72%:28%)** in `.context/rules/` at Positive-Consequence #1 and the Path-1 caveat. Rebutted the "full-path is dominant" implication (bare-ID leads 2.5:1) while conceding full-path is a real ~28% minority (not a lone `ci.yml`). Verified V-4. Retrofitting the rule-corpus full-path citations is [INHERENT]/[P-020] (out of edit mandate). |
| 8 | RT-001 | **FIXED (spec)** | Added **L-12 Grandfather-allowlist freeze** (both files): allowlist frozen at adoption commit, additive-only, no new post-adoption entries — brought under the same audited discipline as the waiver ledger. Actual script build [INHERENT] pending M-6. |
| 9 | FM-101 | **FIXED** | Added a real YAML `---` frontmatter block to the ADR itself (id/scope/origin_project/…), with an HTML comment flagging it as FM-101 self-compliance and honest `id: ADR-PROJ031-004` (current dialect, not the canonical remap target). |
| 10 | CC-001 | **FIXED** | Point-of-claim "designed, not yet built — advisory until M-6" qualifiers added at the ADR L0, ADR L1-testing, and rule-draft Tier-and-Scope present-tense enforcement claims. |
| 11 | IN-002 | **FIXED** | Canonical Location Model "Entity-embedded" row qualified to the **closed `{PROJ\|EPIC\|FEAT\|STORY}` set** (not open-ended `{ENTITY-ID}`) in both files; `BUG-`/`TASK-`/`DISC-`/etc. explicitly excluded. |
| 11 | IN-003 | **FIXED** | Reworded the null-alternative "free and always current" claim: it applies to the filename-grammar-as-discovery-substrate only, NOT the taxonomy-coherence layer (which is the owned "long-term liability" named in L2) — resolving the self-contradiction. |
| 12 | DA-004 | **FIXED** | Restated the promotion evidence as **"3 promoted ADRs from 2 correlated framework-mandate projects, not 3 independent trials"** at the Status, Forces, Rationale-arg-3, and L0 headline restatements (Bimodal section already had it). |
| 13 | PM-101 | **FIXED (empirically corrected)** | M-2b rewritten: `.claude/rules` is a **directory symlink** (V-1), so no per-file symlink step exists; M-2b reduced to a verification, de-gated. Rule-draft wrapper note corrected. |
| 14 | PM-102 | **FRAMED + fallback defined** | Added "Solo-maintainer reality and waiver fallback" (both files): CODEOWNERS single-owner `@geekatron` (V-2) makes the API-verified-second-reviewer waiver non-exercisable today; disclosed honestly + defined an auditable `solo_maintainer: true` fallback gated on CODEOWNERS-resolves-to-one. Actual CODEOWNERS/staffing change [INHERENT]/[P-020]. |
| 15 | PM-103 | **FIXED (spec)** | M-6 and M-13 unified into **one shared `scripts/lint_adr_convention.py` implementation** with two invocation surfaces (Action + CLI); reconciliation point `pyproject.toml:65,72-73`. Actual build [INHERENT]. |
| 16 | RT-004, RT-005 | **FIXED (spec)** | Added **L-11 Waiver-ledger integrity** with numbered rule ID + automatic **expiry re-check** (RT-004) + inclusion in the M-6 regression test (RT-005) in both files. |
| 19 | CC-003 | **FIXED (reconciled)** | Documented the YAML-vs-blockquote parser duality (V-6): the L5 lint parses YAML (new capability scoped into M-6); `jerry ast` blockquote parsing retained for entities/human headers; both coexist on this ADR. Note added to both files. |
| 16 | RT-003 | **FIXED (spec)** | L-1a case-folded look-alike ban **extended** from `{proj\|epic\|feat\|story}` to the full worktracker vocabulary `{proj\|epic\|feat\|story\|enabler\|en\|bug\|task\|spike\|disc\|imp\|dec}` in both files. |
| 17 | FM-104 | **FIXED (softened) + spec** | "Provenance preserved *losslessly*" → "preserved by convention (presence-checked, not accuracy-checked)"; added **L-6b provenance-correctness WARN** to both lint tables. L-6b build [INHERENT] pending M-6. |
| 18 | FM-103 | **FIXED** | Added an explicit **AE-004 scoping clause** to Promotion Path 1: metadata+location-only promotion (immutable body) = C3 lifecycle move, does NOT trip AE-004/C4; a decision-content change is a supersession, fully AE-004-bound. ADR only. |
| 20 | DA-003 | **FRAMED honestly** | Added a Claim-Status: Path 1 is the *designed* default with **zero demonstrated instances** (all history is Path-2; this ADR itself is Path-2/M-9). Named the first real Path-1 candidate (future `ADR-plugin-distribution-001`). "Default path" downgraded to "designed default". Demonstrated instance [INHERENT]. |
| 20 | DA-005 | **FIXED** | M-5b rescoped (Prio 3 edit): owner is **governance, NOT ps-architect**; per-ADR-creation cadence; L-10 lint portion gated via M-6. |
| 21 | CC-004 | **FIXED** | M-7 + rule-draft wrapper NAV-002 citation corrected to **H-23 / NAV-004** (NAV-002 governs a doc's own nav-table placement, not cross-file registration). |
| 21 | FM-107 | **REBUTTED-with-clarification** | The DEPRECATED/SUPERSEDED forward-link asymmetry is **intentional** (DEPRECATED = no specific replacement by definition; a later specific replacement uses SUPERSEDED). No `deprecated_by` field added; reasoning recorded in Status Vocabulary. |
| 21 | DA-006 | **FIXED** | Added a title-slug-tail freeze clause to Path 1 (preserve the full filename tail across the move so full-filename citations survive). |
| 21 | IN-004, FM-105/106/108/109, RT-006/007, DA-007, IN-005, SM-201-205 | **ACKNOWLEDGED / prior-closed** | IN-004 (null-alternative benchmark) already present since iter-2. Remainder are Minor additive-completeness or already-disclosed-residual items (S-003 explicitly labels SM-201-205 "additive not corrective"); addressed by honest framing rather than forced edits, per the remediation guidance for non-load-bearing items. No fabricated closure claimed. |
| 22 | R-6, forward-promotion-rate (PM-009), M-6/M-12 build | **INHERENT (unchanged)** | Already honestly disclosed as monitored-not-closed residuals; the DA-003 Path-1 "designed not demonstrated" framing is now added to this set. No document edit closes them. |

---

## Rebuttals

Items where the finding was judged invalid, mis-scoped, or over-stated, rebutted with cited evidence rather than silently ignored (P-022):

| ID | Finding as scored | Rebuttal (with evidence) | Outcome |
|----|-------------------|--------------------------|---------|
| DA-001 (partial) | Full-path ADR citation is the "*dominant*" style in Jerry's SSOT rule files; the ADR's "overwhelming majority bare-ID" claim is "contradicted." | **Grep over `.context/rules/` (V-4): 28 bare-ID vs 11 full-path (~72%:28%).** Bare-ID *dominates* ~2.5:1, so the "majority is bare-ID" claim is **substantiated, not contradicted**. The finding's valid core — that full-path is more than "a single `ci.yml` example" — is conceded and the caveat widened to the measured ~28%. | Claim re-scoped; "full-path dominant" implication rebutted; "overwhelming" softened. |
| CV-001 (framing) | The iter-2 "~6 not 10" rebuttal is itself wrong; true count is 10. | Both scalars are methodology-dependent (V-3): templated filename grammar = **6 lines**; full non-compliant footprint (title + filename + literal-example + phantom-CLI) = **11 distinct lines**; all-inclusive incl. input/schema = 13. "10" and "~6" are each partial. **Resolution: retire the scalar, publish the grep breakdown** — neither side "wins" a contested integer. | Scalar dispute dissolved with evidence, not defended. |
| FM-107 | Missing `deprecated_by` forward-link is a gap (asymmetric with SUPERSEDED). | By the status definitions, DEPRECATED = "not replaced by a specific ADR"; SUPERSEDED = "replaced by a specific ADR." A DEPRECATED ADR **has no successor to link to by definition**; a later specific replacement is modeled as SUPERSEDED. The asymmetry mirrors a real semantic difference. | Rebutted; no field added; reasoning recorded in Status Vocabulary. |
| FM-101 vs CC-003 (tension) | FM-101 wants YAML frontmatter added; CC-003 notes `jerry ast` reads only blockquote. | Both satisfied without contradiction: YAML `---` added for the L5 lint (FM-101 self-compliance) **and** the blockquote header retained for `jerry ast`/humans; the lint's YAML-parsing is a new capability **scoped into M-6** (V-6). Not an either/or. | Reconciled, both findings closed. |

---

## Tally

- **Deliverables edited:** 2 (`ADR-PROJ031-004-adr-identifier-convention.md`, `adr-standards-rule-draft.md`)
- **Distinct priority-table items dispositioned:** 22 rows (all [FIXABLE-NOW] items edited; all [INHERENT] items honestly framed).
- **`changes` (distinct edit operations across both files + this notes file):** see final reply.
- **`rebuttals` (findings rebutted/re-scoped with evidence rather than accepted at face value):** 4 (DA-001 partial, CV-001 scalar, FM-107, FM-101×CC-003 tension).
- **Fabrication check (P-022):** no Task/Issue IDs invented; no closure claimed for INHERENT residuals (M-6/M-12 build, forward-promotion-rate, R-6, demonstrated Path-1); every factual claim carries a grep/ls-verified citation (V-1..V-7).
- **Constitutional:** P-003 (no subagents spawned), P-020 (only the two mandated deliverables + this notes file edited; `ps-architect.md`, `ci.yml`, `CODEOWNERS`, `worktracker-directory-structure.md`, template/SKILL files left to their owned Migration-Plan items), P-022 (inference labeled; negative consequences and unclosed residuals disclosed).
